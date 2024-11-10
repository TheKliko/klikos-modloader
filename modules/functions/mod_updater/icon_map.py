import re


def get(path: str) -> dict[str,dict[str,dict[str,str|int]]]:
    with open(path, 'r') as file:
        content = file.read()
        file.close()

    data = parse_lua_file(content)
    return data


# ChatGPT
def parse_lua_file(content: str) -> dict[str,dict[str,dict[str,str|int]]]:
    data: dict = {'1x': {}, '2x': {}, '3x': {}}

    # Define a regex pattern to match the asset blocks for each size
    pattern = r"function make_assets_(\dx)\(\).*?(\{.*?\}) end"
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Iterate over the matches to extract the data
    for size, block in matches:
        # Find all the icon definitions within the block
        icon_pattern = r"\['([^']+)'\] = \{ ImageRectOffset = Vector2\.new\((\d+), (\d+)\), ImageRectSize = Vector2\.new\((\d+), (\d+)\), ImageSet = '([^']+)' \}"

        icons = re.findall(icon_pattern, block)
        
        for icon in icons:
            icon_name, x, y, w, h, img_set = icon
            data[size][icon_name] = {
                'set': img_set,
                'x': int(x),
                'y': int(y),
                'w': int(w),
                'h': int(h)
            }
    return data