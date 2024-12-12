import os
import threading
import pathlib
import re
import json
import base64
from io import StringIO
from time import time

import webview


def parse_godot_project(file_path):
    """使用正则表达式解析 Godot project.godot 文件"""
    # 定义正则表达式
    section_pattern = re.compile(r"^\[(.+?)\]$")  # 匹配 [section]
    key_value_pattern = re.compile(r"^([\w/]+)=(.+)$")  # 匹配 key=value

    # 存储解析结果
    result = {}
    current_section = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 去掉空行和注释
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            # 检查是否是一个 section
            section_match = section_pattern.match(line)
            if section_match:
                current_section = section_match.group(1)
                result[current_section] = {}
                continue

            # 检查是否是一个 key=value 对
            key_value_match = key_value_pattern.match(line)
            if key_value_match and current_section:
                key, value = key_value_match.groups()
                # 去掉两侧的引号
                value = value.strip().strip('"')
                result[current_section][key] = value

    return result


class Api:
    def get_settings(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "../settings.json")):
            with open("./settings.json", "r") as f:
                settings = f.read()
            return json.loads(settings)
        return {"godotExecute": ""}

    def save_settings(self, data):
        with open("./settings.json", "w+") as f:
            f.write(json.dumps(data, indent=2))

    def save_export_settings(self, projectPath, settings):
        export_settings_path = os.path.join(projectPath, "minigame.export.json")
        with open(export_settings_path, "w+") as f:
            f.write(json.dumps(settings, indent=2))

    def get_godot_execute(self):
        filename = webview.active_window().create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            allow_multiple=False,
            directory="~",
            file_types=("Godot Execute (*.exe)",),
        )
        if not filename:
            return
        return filename

    def read_projects(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "../projects.json")):
            with open("./projects.json", "r") as f:
                projects = f.read()
                projects = json.loads(projects)
            _projects = []
            for project in projects:
                with open(project["icon"], "rb") as img_file:
                    encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
                project["icon"] = encoded_string
                _projects.append(project)
            return _projects
        return []

    def open_projects(self):
        folder = webview.active_window().create_file_dialog(
            dialog_type=webview.FOLDER_DIALOG, directory="", allow_multiple=False
        )
        folder = folder[0]
        godot_project = os.path.join(folder, "project.godot")

        project_data = parse_godot_project(godot_project)
        application = project_data["application"]
        project = {
            "name": application.get("config/name", ""),
            "path": folder,
            "version": application.get("config/version", ""),
            "description": application.get("config/description", ""),
            "icon": (
                application.get("config/icon", "").split("//")[-1]
                if application.get("config/icon", "")
                else "icon.svg"
            ),
        }
        project["icon"] = os.path.join(folder, project["icon"])
        projects = self.read_projects()
        projects.append(project)
        print(projects)
        with open("./projects.json", "w+") as f:
            json_projects = json.dumps(projects, indent=2)
            f.write(json_projects)
        return projects

    def open_export_path(self, project_path):
        export_folder = webview.active_window().create_file_dialog(
            dialog_type=webview.FOLDER_DIALOG, directory="", allow_multiple=False
        )
        export_folder = pathlib.Path(export_folder[0])
        project_path = pathlib.Path(project_path)
        return export_folder.relative_to(project_path).as_posix()


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists("../gui/index.html"):  # unfrozen development
        return "../gui/index.html"

    if exists("../Resources/gui/index.html"):  # frozen py2app
        return "../Resources/gui/index.html"

    if exists("./gui/index.html"):
        return "./gui/index.html"

    raise Exception("No index.html found")


entry = get_entrypoint()


if __name__ == "__main__":
    window = webview.create_window(
        "pywebview-react boilerplate",
        entry,
        js_api=Api(),
        width=1024,
        height=800,
        min_size=(1024, 800),
    )
    window.settings = {
        "ALLOW_FILE_URLS": True,
        "OPEN_EXTERNAL_LINKS_IN_BROWSER": True,
        "OPEN_DEVTOOLS_IN_DEBUG": True,
    }
    webview.start(debug=True)
