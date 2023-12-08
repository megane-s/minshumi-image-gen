from PIL import ImageDraw
from image.layout import Rect
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


def draw_tags(
    draw: ImageDraw.ImageDraw,
    rect: Rect,
    tags: list[str],
    fill_color,
    text_color,
    v_gap=0,
    h_gap=0,
):
    tag_start_x = rect.left
    tag_start_y = rect.top
    tag_current_x = tag_start_x
    tag_current_y = tag_start_y
    tag_max_h = 0

    for tag in tags:
        tag_w, tag_h = tag_bbox(draw, tag)
        
        if tag_current_x + tag_w < rect.left + rect.width:
            draw_tag(
                draw,
                (
                    tag_current_x,
                    tag_current_y,
                    tag_current_x + tag_w,
                    tag_current_y + tag_h,
                ),
                tag,
                fill=fill_color,
                text=text_color,
            )
            tag_current_x += tag_w
            tag_current_x += h_gap
        else:
            tag_current_x = tag_start_x
            tag_current_y += tag_max_h
            tag_current_y += v_gap
            draw_tag(
                draw,
                (
                    tag_current_x,
                    tag_current_y,
                    tag_current_x + tag_w,
                    tag_current_y + tag_h,
                ),
                tag,
                fill=fill_color,
                text=text_color,
            )
            tag_max_h = tag_h
            tag_current_x += tag_w
            tag_current_x += h_gap
        tag_max_h = tag_h if tag_h > tag_max_h else tag_max_h
