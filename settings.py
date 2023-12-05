from PIL import ImageFont


def get_font(size: int = 24):
    return ImageFont.truetype("./fonts/MPLUS1-Regular.ttf", size)
