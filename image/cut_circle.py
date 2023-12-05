from PIL import Image, ImageDraw


def cut_circle(img: Image.Image):
    background = Image.new("RGBA", img.size)

    mask = Image.new("L", background.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_w, mask_h = mask.size
    mask_draw.ellipse((0, 0, mask_w - 1, mask_h - 1), fill=255)
    mask.save("./test-mask-output.png")

    return Image.composite(img, background, mask)
