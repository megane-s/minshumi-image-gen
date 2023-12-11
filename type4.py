from PIL import Image, ImageDraw
from image.cut import  cut_rounded_rect
from image.flow_layout import draw_text_with_wrap, textbbox_with_wrap
from settings import get_font
from image.layout import  Rect
from colors import colors


NAME_FONT = get_font(60)
ART_FONT = get_font(35)

def _draw_background_filter(img: Image.Image):
    overlay_img = Image.new("RGBA", img.size)
    overlay_draw = ImageDraw.Draw(overlay_img)
    overlay_draw.rectangle(
        (0, 0, 0 + img.width, 0 + img.height), fill=(0, 0, 0, int(255 * 0.3))
    )
    img.alpha_composite(overlay_img)

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
            fill=(255, 255, 255, int(255 * 0.85)),
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
    username,
    icon,
    colors,
):
    draw = ImageDraw.Draw(img)
    arts_rect = get_arts_rect(img)
    summary_bottom = arts_rect.top - 20
    summary_left = 100

    # サイズ計算

    # アイコン
    icon_w, icon_h = (260, 260)


    # 名前
    name_w = tags_w
    name_bbox = textbbox_with_wrap(draw, (0, 0), name_w, username, font=NAME_FONT)
    name_h = name_bbox[3] - name_bbox[1]

    # 全体のサイズ
    summary_h = rank_h + 16 + name_h + 27 + tag_h
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
            int(summary_t + (summary_h / 2 - icon_h / 2)),
        ),
    )  # TODO

    # 名前
    name_bottom = tags_rect.top - 27
    name_top = name_bottom - name_h
    name_left = summary_left
    draw_text_with_wrap(
        draw,
        (name_left, name_top),
        name_w,
        username,
        fill=colors.text.inner,
        font=NAME_FONT,
        stroke_width=5,
        stroke_fill=colors.text.edge,
    )

def businesscard_type_4(
    username,
    icon,
    rank,
    interest_tags,
    arts,
    background_image,
    theme_color,
):
    img = Image.open(background_image)

    _draw_background_filter(img)
    _draw_arts(img, arts, colors[theme_color])
    _draw_summary(img, rank, username, interest_tags, icon, colors[theme_color])

    img.save("output.png")


businesscard_type_4(
    "つーばーさつーばーさ",
    "./placeholder/400x400_green.png",
    "アクションマスター",
    [
        "アクション",
        "SF",
        "恋愛",
        "アニメ",
        "SF",
        "恋愛",
        "SF",
    ],
    ["ずっと真夜中でいいのに。", "かいけつゾロリ", "呪術廻戦"],
    "./placeholder/1200x675_red.png",
    "red",
)
