from PIL import ImageDraw, Image
from colors import BoxColors

from image.layout import Size
from image.text import draw_text


def tagsbox(
    draw: ImageDraw.ImageDraw,
    tags: list[str],
    font,
    width: int = 2**20,
    gap_x: int = 8,
    gap_y: int = 8,
    padding_left: int = 16,
    padding_right: int = 16,
    padding_top: int = 8,
    padding_bottom: int = 8,
):
    left, top = 0, 0
    current_x = left
    current_y = top
    row_max_h = 0
    for tag in tags:
        _, _, text_w, text_h = draw.textbbox(
            xy=(0, 0),
            text=tag,
            font=font,
        )
        tag_w = text_w + padding_left + padding_right
        tag_h = text_h + padding_top + padding_bottom
        newline = left + width <= current_x + tag_w
        if newline:
            current_x = left
            current_y += row_max_h + gap_y
            row_max_h = 0
        current_x += tag_w + gap_x
        row_max_h = max(tag_h, row_max_h)
    return Size(current_x, current_y + row_max_h)


def draw_tags(
    img: Image.Image,
    tags: list[str],
    font,
    colors: BoxColors,
    xy: tuple[int, int],
    gap_x: int = 8,
    gap_y: int = 8,
    width: int = 2**20,
    padding_left: int = 16,
    padding_right: int = 16,
    padding_top: int = 8,
    padding_bottom: int = 8,
):
    draw = ImageDraw.Draw(img)
    left, top = xy
    current_x = left
    current_y = top
    row_max_h = 0
    for tag in tags:
        _, _, text_w, text_h = draw.textbbox(
            xy=(0, 0),
            text=tag,
            font=font,
        )
        tag_w = text_w + padding_left + padding_right
        tag_h = text_h + padding_top + padding_bottom
        newline = left + width <= current_x + tag_w
        if newline:
            current_x = left
            current_y += row_max_h + gap_y
            row_max_h = 0
        draw.rounded_rectangle(
            xy=(current_x, current_y, current_x + tag_w, current_y + tag_h),
            fill=colors.box,
            radius=min(tag_w / 2, tag_h / 2),
        )
        draw_text(
            img,
            text=tag,
            xy=(current_x + padding_left, current_y + padding_top),
            width=tag_w,
            fill=colors.text,
            font=font,
        )
        current_x += tag_w + gap_x
        row_max_h = max(tag_h, row_max_h)
