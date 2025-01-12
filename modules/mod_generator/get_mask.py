from PIL import Image

from .create_gradient_image import create_gradient_image


cache: dict[str, Image.Image] = {}


def get_mask(color1, color2, angle: int, size: tuple[int, int]) -> Image.Image:
    key: str = f"{color1}-{color2}-{angle}-{size[0]}-{size[1]}"
    if key in cache:
        return cache[key]
    
    if color2 is None:
        mask: Image.Image = Image.new("RGBA", size, color1)
    
    else:
        mask = create_gradient_image(size, color1, color2, angle)
    
    cache[key] = mask

    return mask


def clear_cache() -> None:
    cache.clear()