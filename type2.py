from PIL import Image, ImageDraw

from colors import BusinessCardColors, colors
from image.background import draw_background_filter
from image.cut import cut_rounded_rect
from image.flow_layout import draw_text_with_wrap, textbbox_with_wrap
from image.layout import Rect
from settings import get_font
from tag import draw_tags, tag_bbox

RANK_FONT = get_font(40)
NAME_FONT = get_font(65)
TAG_FONT = get_font(35)
ART_FONT = get_font(44)


def get_arts_rect(
    img: Image.Image,
):
    art_h = 170
    return Rect.new_ltwh(
        left=47,
        top=img.height - 34 - art_h,
        w=img.width - 47 * 2,
        h=art_h,
    )


def _draw_arts(
    img: Image.Image,
    arts,
    colors,
):
    art_w = (img.width - 47 - 47 - (20 * 2)) / 3
    arts_rect = get_arts_rect(img)
    for i, art in enumerate(arts):
        art_img = Image.new("RGBA", img.size)
        art_draw = ImageDraw.Draw(art_img)
        art_h = arts_rect.height
        art_x = 47 + (i * art_w) + (i * 20)
        art_y = arts_rect.top
        art_draw.rectangle(
            (art_x, art_y, art_x + art_w, art_y + art_h),
            fill=(255, 255, 255, int(255 * 0.9)),
        )
        draw_text_with_wrap(
            art_draw,
            (art_x + 30, art_y + 30),
            width=art_w - 30 * 2,
            text=art,
            fill=(0, 0, 0),
            font=ART_FONT,
        )
        img.alpha_composite(art_img)


def _draw_summary(
    img: Image.Image,
    rank,
    username,
    interest_tags,
    icon,
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)
    arts_rect = get_arts_rect(img)
    summary_bottom = arts_rect.top - 20
    summary_left = 100

    # サイズ計算

    # アイコン
    icon_w, icon_h = (250, 250)

    # タグ
    tags_w = img.width - 100 - 100 - icon_w - 24

    tag_start_x = 0
    tag_start_y = 0
    tag_current_x = tag_start_x
    tag_current_y = tag_start_y
    tag_max_h = 0

    TAG_H_GAP = 9
    TAG_V_GAP = 9

    if interest_tags is not None:
        for tag in interest_tags:
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
    else:
        tags_h = 50

    # 名前
    name_w = tags_w
    name_bbox = textbbox_with_wrap(
        draw, (0, 0), name_w, username, font=NAME_FONT)
    name_h = name_bbox[3] - name_bbox[1]

    # 称号
    if rank is not None:
        rank_text_bbox = textbbox_with_wrap(
            draw, (0, 0), tags_w, text=rank, font=RANK_FONT
        )
        rank_text_w = rank_text_bbox[2] - rank_text_bbox[0]
        rank_text_h = rank_text_bbox[3] - rank_text_bbox[1]
        rank_w = 0 + rank_text_w + 0
        rank_h = 16 + rank_text_h + 16
    else:
        rank_w = 0
        rank_h = 0

    # 全体のサイズ
    summary_h = rank_h + 16 + name_h + 27 + tags_h
    summary_t = summary_bottom - summary_h

    # 描画
    # アイコン
    icon_img = Image.open(icon)
    icon_img = icon_img.resize((icon_w, icon_h))
    icon_img = cut_rounded_rect(icon_img, 60)
    img.alpha_composite(
        icon_img,
        dest=(
            int(img.width - 100 - icon_w),
            # int(summary_t + (summary_h / 2 - icon_h / 2)),
            summary_bottom - tags_h - icon_h - 20,
        ),
    )  # TODO

    # タグ
    tags_rect = Rect.new_ltwh(
        left=summary_left,
        top=summary_bottom - tags_h,
        w=tags_w,
        h=tags_h,
    )
    if interest_tags is not None:
        draw_tags(
            draw,
            rect=tags_rect,
            tags=interest_tags,
            fill_color=colors.label.box,
            text_color=colors.label.text,
            v_gap=16,
            h_gap=12,
        )

    # 名前
    name_bottom = tags_rect.top - 27
    name_top = name_bottom - name_h
    name_left = summary_left
    draw_text_with_wrap(
        draw,
        (name_left, name_top),
        name_w,
        username,
        fill=colors.text.bordered.inner,
        font=NAME_FONT,
        stroke_width=5,
        stroke_fill=colors.text.bordered.edge,
    )

    # 称号
    rank_bottom = name_top - 16
    rank_top = rank_bottom - rank_h
    rank_left = summary_left
    rank_right = rank_left + 40 + rank_w + 40
    if rank is not None:
        draw.rounded_rectangle(
            (rank_left, rank_top, rank_right, rank_top + rank_h),
            radius=int(rank_h / 2),
            fill=colors.label.box,
        )

    if rank is not None:
        rank_text_left = rank_left + 40
        rank_text_top = rank_top + 16
        draw_text_with_wrap(
            draw,
            (rank_text_left, rank_text_top),
            width=tags_w,
            text=rank,
            fill=colors.label.text,
            font=RANK_FONT,
        )


def businesscard_type_2(
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

    img = draw_background_filter(img)
    _draw_arts(img, arts, colors[theme_color])
    _draw_summary(img, rank, username, interest_tags,
                  icon, colors[theme_color])

    # img.save("output.png")
    return img


# businesscard_type_2(
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
