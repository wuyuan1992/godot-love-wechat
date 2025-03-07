import json
import os
from typing import List
import zipfile
from app import gdscripts
from app.stroge import Storge
import boto3
from botocore.config import Config
from pathlib import Path
import subprocess


class Exporter:
    def __init__(self) -> None:
        self.storage: Storge = Storge()

    def get_tempalte_json(self):
        with open("./templates/template.json", "rb") as f:
            templates = json.loads(f.read())
        return templates

    def get_export_settings(self, project: dict):
        p = os.path.join(project["path"], "minigame.export.json")
        if not os.path.exists(p):
            return {}
        with open(p, "rb") as f:
            export_settings = json.loads(f.read())
            export_settings["export_path"] = os.path.join(
                project["path"], export_settings["export_path"]
            )
        return export_settings

    def export_project(self, export_settings: dict, project: dict):
        exported = os.path.exists(
            os.path.join(export_settings["export_path"], "game.json")
        )
        self.save_export_settings(export_settings, project["path"])
        settings = self.storage.get("settings.json")

        if exported and settings:
            if export_settings["subpack_config"]:
                self.export_subpack(
                    export_settings["subpack_config"],
                    export_settings,
                    project["path"],
                    settings["godot_execute"],
                )
            else:
                gdscripts.set_export_presets(
                    settings["godot_execute"],
                    project["path"],
                    export_settings["export_perset"],
                    config_index=None,
                )
                pckPath = os.path.join(
                    export_settings["export_path"], "engine\\godot.zip"
                )
                self.export_pck(project["path"], export_settings, pckPath)
        else:
            with zipfile.ZipFile(
                f"./templates/{export_settings['export_template']}"
            ) as zf:
                zf.extractall(export_settings["export_path"])

            pckPath = os.path.join(export_settings["export_path"], "engine\\godot.zip")
            self.replace_gamejson(export_settings)
            self.replace_privatejson(project, export_settings)
            if export_settings["subpack_config"]:
                self.export_subpack(
                    export_settings["subpack_config"],
                    export_settings,
                    project["path"],
                    settings["godot_execute"],  # pyright: ignore
                )
            else:
                gdscripts.set_export_presets(
                    settings["godot_execute"],  # pyright: ignore
                    project["path"],
                    export_settings["export_perset"],
                    config_index=None,
                )
                pckPath = os.path.join(
                    export_settings["export_path"], "engine\\godot.zip"
                )
                self.export_pck(project["path"], export_settings, pckPath)

    def replace_gamejson(self, export_settings: dict):
        path = os.path.join(export_settings["export_path"], "game.json")
        with open(path, "rb") as f:
            gamejson = json.loads(f.read())
            gamejson["deviceOrientation"] = export_settings["device_orientation"]
        with open(path, "w+") as f:
            f.write(json.dumps(gamejson, indent=2))

    def replace_privatejson(self, project: dict, export_settings: dict):
        path = os.path.join(
            export_settings["export_path"], "project.private.config.json"
        )
        with open(path, "rb") as f:
            privatejson = json.loads(f.read())
            privatejson["projectname"] = project.get("name", "")
            privatejson["description"] = project.get("description", "")
            privatejson["appid"] = export_settings.get("appid", "")
        with open(path, "w+") as f:
            f.write(json.dumps(privatejson, indent=2))

    def save_export_settings(self, export_settings: dict, project_path: str):
        projectpath = Path(project_path)
        with open(projectpath.joinpath("minigame.export.json"), "w+") as f:
            f.write(json.dumps(export_settings, indent=2))

    def export_pck(self, project_path: str, export_settings: dict, packPath: str):
        settings = self.storage.get("settings.json")
        if settings:
            godot_execute = settings["godot_execute"]
            result = subprocess.run(
                [
                    godot_execute,
                    "--headless",
                    "--path",
                    project_path,
                    "--export-pack",
                    export_settings["export_perset"],
                    packPath,
                ]
            )
            print(result)

    def preview_project(self, export_settings: dict):
        export_path = export_settings["export_path"]
        settings = self.storage.get("settings.json")
        if settings:
            wechat_execute = os.path.join(settings["wechat_execute"], "cli.bat")
            result = subprocess.run([wechat_execute, "open", "--project", export_path])
            print(result)

    def export_subpack(
        self,
        subpacks: List[dict],
        export_settings: dict,
        project_path: str,
        godot_execute: str,
    ):
        localpath = Path().absolute().resolve().as_posix()
        settings = self.storage.get("settings.json")
        if settings:
            s3client = boto3.client(
                "s3",
                aws_access_key_id=settings["cdn_access_key_id"],
                aws_secret_access_key=settings["cdn_secret_access_key"],
                aws_session_token=settings["cdn_session_token"],
                endpoint_url=settings["cdn_endpoint"],
                config=Config(
                    s3={"addressing_style": "virtual"}, signature_version="v4"
                ),
            )
            for i, pack in enumerate(subpacks):
                gdscripts.set_export_presets(
                    godot_execute, project_path, export_settings["export_perset"], i
                )
                if pack["subpack_type"] == "main":
                    pckPath = os.path.join(
                        export_settings["export_path"], "engine\\godot.zip"
                    )
                    self.export_pck(project_path, export_settings, pckPath)
                if pack["subpack_type"] == "inner_subpack":
                    pckPath = os.path.join(
                        export_settings["export_path"], f"subpacks\\{pack['name']}.zip"
                    )
                    self.export_pck(project_path, export_settings, pckPath)

                if pack["subpack_type"] == "cdn_subpack":
                    pckPath = os.path.join(localpath, f"tmp\\{pack['name']}.zip")
                    self.export_pck(project_path, export_settings, pckPath)
                    s3client.upload_file(
                        pckPath, export_settings["bucket"], pack["cdn_path"]
                    )
