import json
import os
import zipfile
from app.stroge import Storge
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
            export_settings["export_path"] = os.path.join(project["path"], export_settings["export_path"])
        return export_settings

    def export_project(self, export_settings: dict, project: dict):
        exported = os.path.exists(os.path.join(export_settings["export_path"], "game.json"))
        if exported:
            self.export_pck(project["path"], export_settings)
        else:
            with zipfile.ZipFile(f"./templates/{export_settings['export_template']}") as zf:
                zf.extractall(export_settings["export_path"])
            self.export_pck(project["path"], export_settings)
            self.replace_gamejson(export_settings)
            self.replace_privatejson(project, export_settings)
            self.save_export_settings(export_settings, project["path"])

    def replace_gamejson(self, export_settings: dict):
        path = os.path.join(export_settings["export_path"], "game.json")
        with open(path, "rb") as f:
            gamejson = json.loads(f.read())
            gamejson["deviceOrientation"] = export_settings["device_orientation"]
        with open(path, "w+") as f:
            f.write(json.dumps(gamejson, indent=2))

    def replace_privatejson(self, project: dict, export_settings: dict):
        path = os.path.join(export_settings["export_path"], "project.private.config.json")
        with open(path, "rb") as f:
            privatejson = json.loads(f.read())
            privatejson["projectname"] = project.get("name", "")
            privatejson["description"] = project.get("description", "")
            privatejson["appid"] = export_settings.get("appid", "")
        with open(path, "w+") as f:
            f.write(json.dumps(privatejson, indent=2))

    def save_export_settings(self, export_settings: dict, project_path: str):
        export_path = Path(export_settings["export_path"])
        projectpath = Path(project_path)
        relative_export_path = export_path.relative_to(projectpath).as_posix()
        export_settings["export_path"] = relative_export_path
        with open(projectpath.joinpath("minigame.export.json"), "w+") as f: 
            f.write(json.dumps(export_settings, indent=2))

    def export_pck(self, project_path: str, export_settings: dict):
        pckPath = os.path.join(export_settings["export_path"], "engine\\godot.zip")
        settings = self.storage.get("settings.json")
        if settings:
            godot_execute = settings["godot_execute"]
            result = subprocess.run([
                godot_execute,
                "--headless",
                "--path",
                project_path,
                "--export-pack",
                "Web",
                pckPath,
            ])   
            print(result)

    def preview_project(self, export_settings: dict):
        export_path = export_settings["export_path"]
        settings = self.storage.get("settings.json")
        if settings:
            wechat_execute = os.path.join(settings["wechat_execute"], "cli.bat")
            result = subprocess.run([
                wechat_execute,
                "open",
                "--project",
                export_path
            ])
            print(result)
