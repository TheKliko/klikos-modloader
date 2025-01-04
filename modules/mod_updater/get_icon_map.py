from pathlib import Path
import re


def get_icon_map(filepath: Path) -> dict[str, dict[str, dict[str, str | int]]]:
    with open(filepath, "r") as file:
        content: str = file.read()

    return parse_file_content(content)


# ChatGPT
def parse_file_content(content: str) -> dict[str, dict[str, dict[str, str | int]]]:
    icon_map: dict[str, dict[str, dict[str, str | int]]] = {}

    image_size_pattern: str = r"function make_assets_(\dx)\(\).*?(\{.*?\}) end"
    icon_data_pattern: str = r"\['([^']+)'\] = \{ ImageRectOffset = Vector2\.new\((\d+), (\d+)\), ImageRectSize = Vector2\.new\((\d+), (\d+)\), ImageSet = '([^']+)' \}"

    image_size_matches: list = re.findall(image_size_pattern, content, re.DOTALL)
    for size, data in image_size_matches:
        if size not in icon_map:
            icon_map[size] = {}
        
        icon_data_matches: list = re.findall(icon_data_pattern, data)
        for icon in icon_data_matches:
            name, x, y, w, h, image_set = icon
            icon_map[size][name] = {
                "image_set": image_set,
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }

    return icon_map