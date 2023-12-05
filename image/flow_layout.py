from PIL import ImageDraw


def textbbox_with_wrap(
    draw: ImageDraw.ImageDraw,
    xy,
    width,
    text: str,
    fill=None,
    font=None,
    spacing=4,
    stroke_width=0,
    stroke_fill=None,
):
    chars = list(text)
    start_x, start_y = xy
    current_x, current_y = xy
    max_h = 0

    for char in chars:
        _, _, char_w, char_h = draw.textbbox(
            (0, 0),
            text=char,
            font=font,
            spacing=spacing,
            stroke_width=stroke_width,
        )
        if current_x + char_w < start_x + width:
            # 横に並べる
            current_x += char_w
        else:
            # 改行
            current_x = start_x
            current_y += max_h
            max_h = 0
            current_x += char_w
        max_h = char_h if char_h > max_h else max_h
    return (start_x, start_y, start_x + width, current_y + max_h)


def draw_text_with_wrap(
    draw: ImageDraw.ImageDraw,
    xy,
    width,
    text: str,
    fill=None,
    font=None,
    spacing=4,
    stroke_width=0,
    stroke_fill=None,
):
    chars = list(text)
    start_x, start_y = xy
    current_x, current_y = xy
    max_h = 0

    for char in chars:
        _, _, char_w, char_h = draw.textbbox(
            (0, 0),
            text=char,
            font=font,
            spacing=spacing,
            stroke_width=stroke_width,
        )
        if current_x + char_w < start_x + width:
            # 横に並べる
            draw.text(
                (current_x, current_y),
                text=char,
                font=font,
                spacing=spacing,
                stroke_width=stroke_width,
                fill=fill,
                stroke_fill=stroke_fill,
            )
            current_x += char_w
        else:
            # 改行
            current_x = start_x
            current_y += max_h
            draw.text(
                (current_x, current_y),
                text=char,
                font=font,
                spacing=spacing,
                stroke_width=stroke_width,
                fill=fill,
                stroke_fill=stroke_fill,
            )
            max_h = char_h
            current_x += char_w
        max_h = char_h if char_h > max_h else max_h
