from PIL import Image, ImageDraw


def draw_background_filter(img: Image.Image, opacity: float = 0.2):
    overlay_img = Image.new("RGBA", img.size)
    overlay_draw = ImageDraw.Draw(overlay_img)
    overlay_draw.rectangle(
        (0, 0, 0 + img.width, 0 + img.height),
        fill=(0, 0, 0, int(255 * opacity)),
    )
    img.alpha_composite(overlay_img)
