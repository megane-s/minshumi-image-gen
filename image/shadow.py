from PIL import Image, ImageDraw, ImageFilter

from image.flow_layout import draw_text_with_wrap


def draw_text_with_shadow(
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
    shadow_radius=4,
    shadow_x=0,
    shadow_y=0,
):
    x, y = xy
    # 影描画
    shadow_img = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(shadow_img)
    draw_text_with_wrap(
        draw,
        xy=(x + shadow_x, y + shadow_y),
        width=width,
        text=text,
        fill=shadow_color,
        font=font,
        stroke_width=stroke_width,
        stroke_fill=shadow_color,
    )
    shadow_img = shadow_img.filter(
        filter=ImageFilter.GaussianBlur(radius=shadow_radius)
    )
    img.alpha_composite(shadow_img)

    # 文字を描画
    draw = ImageDraw.Draw(img)
    draw_text_with_wrap(
        draw,
        xy=xy,
        width=width,
        text=text,
        fill=fill,
        font=font,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
