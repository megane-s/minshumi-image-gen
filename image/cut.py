from PIL import Image, ImageDraw


def cut_circle(img: Image.Image):
    background = Image.new("RGBA", img.size)

    mask = Image.new("L", background.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_w, mask_h = mask.size
    mask_draw.ellipse((0, 0, mask_w - 1, mask_h - 1), fill=255)

    return Image.composite(img, background, mask)


def cut_rounded_rect(img: Image.Image, radius: int):
    background = Image.new("RGBA", img.size)

    mask = Image.new("L", background.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_w, mask_h = mask.size
    mask_draw.rounded_rectangle((0, 0, mask_w - 1, mask_h - 1), radius=radius, fill=255)

    return Image.composite(img, background, mask)
