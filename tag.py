from PIL import ImageDraw
from settings import get_font


def tag_bbox(
    draw: ImageDraw.ImageDraw,
    tag: str,
):
    l, t, r, b = draw.textbbox(
        (0, 0),
        text=tag,
        font=get_font(35),
    )
    return (r + 31 + 31, b + 11 + 11)


def draw_tag(
    draw: ImageDraw.ImageDraw,
    rect,
    tag: str,
    fill,
    text,
):
    container_left, container_top, container_right, container_bottom = rect
    draw.rounded_rectangle(
        (container_left, container_top, container_right, container_bottom),
        radius=(container_bottom - container_top) / 2,
        fill=fill,
    )
    draw.text(
        (31 + container_left, 11 + container_top),
        tag,
        fill=text,
        font=get_font(35),
    )
