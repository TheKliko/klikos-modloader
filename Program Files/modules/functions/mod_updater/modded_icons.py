import copy
import os

from PIL import Image


DEFAULT: dict[str,list] = {
    "1x": [],
    "2x": [],
    "3x": []
}


def get(mod_path, version_path, imageset_path: str, icon_map: dict[str,dict[str,dict[str,str|int]]]) -> dict[str,list[str]]:
    modded_icons: dict[str,list] = copy.deepcopy(DEFAULT)

    for size, icons in icon_map.items():
        for name, data in icons.items():
            relative_path: str = os.path.join(imageset_path, str(data["set"]))+".png"
            
            unmodded_path: str = os.path.join(version_path, relative_path)
            modded_path: str = os.path.join(mod_path, relative_path)

            if not os.path.isfile(modded_path):
                continue

            x: int = int(data["x"])
            y: int = int(data["y"])
            w: int = int(data["w"])
            h: int = int(data["h"])

            with Image.open(unmodded_path) as image1:
                icon1 = image1.crop((x,y,x+w,y+h))
            with Image.open(modded_path) as image2:
                icon2 = image2.crop((x,y,x+w,y+h))

            if is_modded_image(image1=icon1, image2=icon2):
                modded_icons[size].append(name)

                # print("Modded icon detected: "+str(name))
                # with Image.new("RGBA", (w*2, h)) as preview_image:
                #     preview_image.paste(icon1,(0,0))
                #     preview_image.paste(icon2, (w,0))
                #     preview(preview_image)

    return modded_icons


def is_modded_image(image1: Image.Image, image2: Image.Image) -> bool:
    if image1.size != image2.size or image1.format != image2.format:
        return False
    
    pixels1 = image1.load()
    pixels2 = image2.load()

    for y in range(image1.height):
        for x in range(image1.width):
            pixel1 = pixels1[x, y]
            pixel2 = pixels2[x, y]

            if image1.format == "PNG":
                if pixel1[3] == 0 and pixel2[3] == 0:
                    continue

            if pixel1 != pixel2:
                return True
    
    return False


# Used for debugging
def preview(image: Image.Image) -> None:
    import time
    if isinstance(image, Image.Image):
        image.show()
        time.sleep(2)
        os.system("taskkill /f /im Photos.exe >nul 2>&1")
    
    else:
        print('Unable to preview image')