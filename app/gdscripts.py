from pathlib import Path
import subprocess
import json
import re


def get_export_presets(godot_execute: str, project_path: str):
    abs = Path().resolve().resolve()
    script_path = abs.joinpath("gdscripts/export_perset.gd")

    result = subprocess.run(
        [
            godot_execute,
            "--headless",
            "--path",
            project_path,
            "-d",
            "--script",
            script_path.as_posix(),
        ],
        capture_output=True,
        text=True,
    )
    output = result.stdout
    match = re.search(r"\[.*?\]", output)
    if match:
        json_str = match.group()
        return json.loads(json_str)
    else:
        return []


def set_export_presets(
    godot_execute: str, project_path: str, preset: str, config_index: int
):
    abs = Path().resolve().resolve()
    script_path = abs.joinpath("gdscripts/set_preset.gd")

    result = subprocess.run(
        [
            godot_execute,
            "--headless",
            "--path",
            project_path,
            "-d",
            "--script",
            script_path.as_posix(),
            "--",
            preset,
            str(config_index),
        ],
        capture_output=True,
        text=True,
    )
    output = result.stdout
    return output
