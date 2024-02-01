from PIL import Image, ImageDraw

from colors import BusinessCardColors, colors
from image.background import draw_background_filter
from image.cut import cut_circle, cut_rounded_rect
from image.flow_layout import draw_text_with_wrap, textbbox_with_wrap
from image.layout import Rect
from settings import get_font

NAME_FONT = get_font(90)
ART_FONT = get_font(40)


def _draw_icon_and_name(
    img: Image.Image,
    icon,
    username,
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズ計算

    # アイコンのサイズ
    icon_w, icon_h = (260, 260)

    # 名前のサイズ
    _, _, name_w, name_h = textbbox_with_wrap(
        draw=draw,
        xy=(0, 0),
        width=img.width,
        text=username,
        font=NAME_FONT,
        stroke_width=5,
    )

    # 位置計算
    icon_x = img.width / 2 - icon_w / 2
    icon_y = 70
    name_x = img.width / 2 - name_w / 2
    name_y = img.height - 70 - icon_h - 10

    # 描画
    # アイコンの描画
    icon_img = Image.open(icon)
    icon_img = cut_circle(icon_img.resize((icon_w, icon_h)))
    img.alpha_composite(icon_img, dest=(int(icon_x), int(icon_y)))

    # 名前の描画
    draw_text_with_wrap(
        draw=draw,
        xy=(name_x, name_y),
        width=img.width,
        text=username,
        font=NAME_FONT,
        stroke_width=5,
        fill=colors.text.bordered.inner,
        stroke_fill=colors.text.bordered.edge,
    )

    pass


def get_arts_rect(
    img: Image.Image,
):
    art_h = 157
    return Rect.new_ltwh(
        left=40,
        top=img.height - 38 - art_h,
        w=img.width - 40 * 2,
        h=art_h,
    )


def _draw_arts(
    img: Image.Image,
    arts,
    color: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズ計算
    art_width, art_height = (350, 157)
    arts_h_gap = 35  # 37.5

    # 位置計算
    arts_left = img.width
    arts_bottom = 38
    arts_top = img.height - arts_bottom - art_height

    # 背景（作品）描画
    art_w = (img.width - 40 - 40 - (35 * 2)) / 3
    arts_rect = get_arts_rect(img)
    for i, art in enumerate(arts):
        art_img = Image.new("RGBA", img.size)
        art_draw = ImageDraw.Draw(art_img)
        art_h = arts_rect.height
        art_x = 40 + (i * art_w) + (i * 35)
        art_y = arts_rect.top
        art_draw.rectangle(
            (art_x, art_y, art_x + art_w, art_y + art_h),
            fill=(255, 255, 255, int(255 * 0.85)),
        )
        # 描画
        draw_text_with_wrap(
            art_draw,
            (art_x + 30, art_y + 30),
            width=art_w - 30 * 2,
            text=art,
            fill=(0, 0, 0),
            font=ART_FONT,
        )
        img.alpha_composite(art_img)

    pass


def businesscard_type_3(
    username,
    icon,
    rank,
    interest_tags,
    arts,
    background_image,
    theme_color,
):
    img: Image.Image = Image.open(background_image)
    img = img.convert("RGBA")
    img = img.resize((1200, 675))

    draw_background_filter(img)

    _draw_icon_and_name(
        img=img,
        icon=icon,
        username=username,
        colors=colors[theme_color],
    )

    _draw_arts(
        img=img,
        arts=arts,
        color=colors[theme_color],
    )

    return img


# businesscard_type_3(
#     "つーばーさつーばーさ",
#     "./placeholder/400x400_green.png",
#     "アクションマスター",
#     [
#         "アクション",
#         "SF",
#         "恋愛",
#         "アニメ",
#         "SF",
#         "恋愛",
#         "SF",
#     ],
#     ["ずっと真夜中でいいのに。", "かいけつゾロリ", "呪術廻戦"],
#     "./placeholder/1200x675_red.png",
#     "red",
# )
