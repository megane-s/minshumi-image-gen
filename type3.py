from PIL import Image, ImageDraw

from colors import BusinessCardColors, colors
from image.alpha import AlphaCompositeContext
from image.cut import cut_circle, cut_rounded_rect
from image.flow_layout import draw_text_with_wrap, textbbox_with_wrap
from image.layout import Rect
from settings import get_font
from tag import draw_tags, tag_bbox

NAME_FONT = get_font(60)
RANK_FONT = get_font(40)
TAG_FONT = get_font(35)
ART_FONT = get_font(35)


def _draw_background_filter(img: Image.Image):
    overlay_img = Image.new("RGBA", img.size)
    overlay_draw = ImageDraw.Draw(overlay_img)
    overlay_draw.rectangle(
        (0, 0, 0 + img.width, 0 + img.height), fill=(0, 0, 0, int(255 * 0.3))
    )
    img.alpha_composite(overlay_img)


def _draw_icon_and_name(
    img: Image.Image,
    icon,
    username,
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズ計算

    # アイコンのサイズ
    icon_w, icon_h = (250, 250)

    # 名前のサイズ
    _, _, name_w, name_h = textbbox_with_wrap(
        draw=draw,
        xy=(0, 0),
        width=400,
        text=username,
        font=NAME_FONT,
        stroke_width=5,
    )

    # 位置計算
    name_x = (img.width / 2) / 2 - name_w / 2
    name_y = img.height - 86 - name_h
    icon_x = name_x + (name_w / 2 - icon_w / 2)
    icon_y = 86

    # 描画

    # アイコンの描画
    icon_img = Image.open(icon)
    icon_img = cut_circle(icon_img.resize((icon_w, icon_h)))
    img.alpha_composite(icon_img, dest=(int(icon_x), int(icon_y)))

    # 名前の描画
    draw_text_with_wrap(
        draw=draw,
        xy=(name_x, name_y),
        width=400,
        text=username,
        font=NAME_FONT,
        stroke_width=5,
        fill=colors.text.inner,
        stroke_fill=colors.text.edge,
    )


def _draw_details(
    img: Image.Image,
    rank,
    tags,
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズ計算

    # 称号のサイズ
    _, _, rank_text_w, rank_text_h = textbbox_with_wrap(
        draw,
        xy=(0, 0),
        width=img.width / 2 - 50 - 32,
        text=rank,
        font=RANK_FONT,
    )
    # 高さ
    rank_w = 60 + rank_text_w + 60
    rank_h = 16 + rank_text_h + 16

    # タグのサイズ
    tags_w = img.width / 2 - 50 - 32

    tag_start_x = 0
    tag_start_y = 0
    tag_current_x = tag_start_x
    tag_current_y = tag_start_y
    tag_max_h = 0

    TAG_H_GAP = 9
    TAG_V_GAP = 19

    for tag in tags:
        tag_w, tag_h = tag_bbox(
            draw,
            tag,
        )
        if tag_current_x + tag_w < tag_start_x + tags_w:
            # 横に並べる
            tag_current_x += tag_w
            tag_current_x += TAG_H_GAP
        else:
            # 改行
            tag_current_x = tag_start_x
            tag_current_y += tag_max_h
            tag_current_y += TAG_V_GAP
            tag_max_h = tag_h
            tag_current_x += tag_w
            tag_current_x += TAG_H_GAP
        tag_max_h = tag_h if tag_h > tag_max_h else tag_max_h

    tags_h = tag_current_y + tag_max_h

    # 位置計算

    # 称号の位置
    rank_x = img.width / 2 + 50
    rank_y = 50

    # タグの位置
    tags_x = img.width / 2 + 50
    tags_y = rank_y + rank_h + 19

    # 描画

    # 称号の描画
    draw.rectangle(
        (rank_x, rank_y, rank_x + rank_w, rank_y + rank_h),
        fill=colors.label.box,
    )
    draw_text_with_wrap(
        draw=draw,
        xy=(rank_x + 60, rank_y + 16),
        width=img.width / 2 - 50 - 32,
        text=rank,
        font=RANK_FONT,
        fill=colors.label.text,
    )

    # タグの描画
    # TODO タグの数や文字数によっては下にはみ出てしまう
    # TODO 横にはみ出たときに「...」にする
    draw_tags(
        draw=draw,
        rect=Rect.new_ltrb(tags_x, tags_y, tags_x + tags_w, tags_y + tags_h),
        tags=tags,
        fill_color=colors.label.box,
        text_color=colors.label.text,
        v_gap=TAG_V_GAP,
        h_gap=TAG_H_GAP,
    )


def _draw_arts(
    img: Image.Image,
    arts,
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズの計算
    art_width, art_height = (268, 200)
    arts_h_gap = 32

    # 位置の計算
    arts_left = img.width / 2
    arts_bottom = 86
    arts_top = img.height - arts_bottom - art_height

    # 描画

    overlay = Image.new("RGBA", img.size)
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        xy=(arts_left, arts_top, arts_left + art_width, arts_top + art_height),
        fill=(255, 255, 255, int(255 * 0.85)),
    )
    overlay_draw.rectangle(
        xy=(
            arts_left + art_width + arts_h_gap,
            arts_top,
            arts_left + art_width + arts_h_gap + art_width,
            arts_top + art_height,
        ),
        fill=(255, 255, 255, int(255 * 0.85)),
    )
    img.alpha_composite(overlay)

    draw_text_with_wrap(
        draw=draw,
        xy=(arts_left + 30, arts_top + 30),
        width=art_width - 30 - 30,
        text=arts[0],
        fill=(0, 0, 0),
        font=ART_FONT,
    )

    draw_text_with_wrap(
        draw=draw,
        xy=(
            arts_left + art_width + arts_h_gap + 30,
            arts_top + 30,
        ),
        width=art_width - 30 - 30,
        text=arts[1],
        fill=(0, 0, 0),
        font=ART_FONT,
    )


def businesscard_type_3(
    username,
    icon,
    rank,
    interest_tags,
    arts,  # 合計文字数が12文字になるまで
    background_image,
    theme_color,
):
    img :Image.Image = Image.open(background_image)
    img = img.convert("RGBA")
    img = img.resize((1200, 675))
    _draw_background_filter(img)

    _draw_icon_and_name(
        img,
        icon=icon,
        username=username,
        colors=colors[theme_color],
    )
    _draw_details(
        img,
        rank=rank,
        tags=interest_tags,
        colors=colors[theme_color],
    )
    _draw_arts(
        img,
        arts=arts,
        colors=colors[theme_color],
    )

    # img.save("output.png")
    return img


# businesscard_type_3(
#     "つーばーさつーばーさ",
#     "./placeholder/400x400_green.png",
#     # "アクションマスター",
#     "称号",
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
#     "blue",
# )
