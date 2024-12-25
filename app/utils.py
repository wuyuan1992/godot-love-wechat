import re
from PIL import Image

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

def read_icon_to_base64(icon_path):
    with Image.open(icon_path) as img:
        img = img.convert("RGB")
    return img
