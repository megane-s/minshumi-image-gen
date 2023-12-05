from PIL import Image
from image.shadow import draw_text_with_shadow


def draw_text(
    img: Image.Image,
    xy,
    width,
    text: str,
    fill=None,
    font=None,
    spacing=4,
    stroke_width=0,
    stroke_fill=None,
    shadow_color=(0, 0, 0, int(255 * 0.5)),
    shadow_radius=0,
    shadow_x=0,
    shadow_y=0,
):
    draw_text_with_shadow(
        img=img,
        xy=xy,
        width=width,
        text=text,
        fill=fill,
        font=font,
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
        shadow_color=shadow_color,
        shadow_radius=shadow_radius,
        shadow_x=shadow_x,
        shadow_y=shadow_y,
    )
