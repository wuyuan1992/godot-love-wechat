from pathlib import Path
import subprocess
import json
import re


def get_export_presets(godot_execute: str, project_path: str):
    # 注释原本的实现
    # abs = Path().resolve().resolve()
    # script_path = abs.joinpath("gdscripts/export_perset.gd")

    # result = subprocess.run(
    #     [
    #         godot_execute,
    #         "--headless",
    #         "--path",
    #         project_path,
    #         "-d",
    #         "--script",
    #         script_path.as_posix(),
    #     ],
    #     capture_output=True,
    #     text=True,
    # )
    # output = result.stdout
    # match = re.search(r"\[.*?\]", output)
    # if match:
    #     json_str = match.group()
    #     return json.loads(json_str)
    # else:
    #     return []
    
    # 直接返回默认值
    return ['Web']


def set_export_presets(
    godot_execute: str, project_path: str, preset: str, config_index: int | None
):
    # 注释原本的实现
    # abs = Path().resolve().resolve()
    # script_path = abs.joinpath("gdscripts/set_preset.gd")
    # if config_index is None:
    #     result = subprocess.run(
    #         [
    #             godot_execute,
    #             "--headless",
    #             "--path",
    #             project_path,
    #             "-d",
    #             "--script",
    #             script_path.as_posix(),
    #             "--",
    #             preset,
    #         ],
    #         capture_output=True,
    #         text=True,
    #     )
    #     output = result.stdout
    #     return output
    # else:
    #     result = subprocess.run(
    #         [
    #             godot_execute,
    #             "--headless",
    #             "--path",
    #             project_path,
    #             "-d",
    #             "--script",
    #             script_path.as_posix(),
    #             "--",
    #             preset,
    #             str(config_index),
    #         ],
    #         capture_output=True,
    #         text=True,
    #     )
    #     output = result.stdout
    #     return output
    
    # 直接返回默认值
    return 'Web'
