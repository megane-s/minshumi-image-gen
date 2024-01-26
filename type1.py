from PIL import Image, ImageDraw

from colors import BusinessCardColors, colors
from image.cut import cut_circle
from image.flow_layout import textbbox_with_wrap
from image.layout import Offset, Padding, Rect, Size
from image.shadow import draw_text_with_shadow
from image.tag import draw_tags, tagsbox
from image.text import draw_text
from settings import get_font
from tag import draw_tag, tag_bbox

FONT = get_font(32)
NAME_FONT = get_font(72)
RANK_FONT = get_font(36)

LABEL_TEXT = "好きな作品"


def get_label_text_size(img: Image.Image, label_text=LABEL_TEXT):
    draw = ImageDraw.Draw(img)
    label_text_box = draw.textbbox((0, 0), label_text, font=FONT)
    label_text_size = Size(
        label_text_box[2],
        label_text_box[3],
    )
    return label_text_size


def get_label_rect(img: Image.Image, label_text=LABEL_TEXT):
    # label textのサイズを取得
    label_text_size = get_label_text_size(img, label_text)
    label_bg_size = Size.new_wh(w=label_text_size.h + 12 + 12, h=img.height)
    label_bg_rect = Rect.new_offset_size(
        Offset(img.width / 2 - label_bg_size.w / 2, 0),
        label_bg_size,
    )
    return label_bg_rect


def _draw_label(
    img: Image.Image,
    label_color,
):
    draw = ImageDraw.Draw(img)

    # label textのサイズを取得
    label_rect = get_label_rect(img)
    label_text_size = get_label_text_size(img)

    draw.rectangle(label_rect.to_tuple(), fill=label_color.box)

    text_img = Image.new("RGBA", (label_text_size.w, label_text_size.h))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text(
        xy=(0, 0),
        text=LABEL_TEXT,
        fill=label_color.text,
        font=FONT,
    )
    text_img = text_img.rotate(90, expand=True)
    text_img.save("test-text_img-output.png")

    img.alpha_composite(
        text_img,
        (
            int(img.width / 2 - text_img.width / 2),
            int(img.height / 2 - text_img.height / 2),
        ),
    )


def _draw_summary(
    img: Image.Image,
    icon: str,
    username: str,
    rank: str | None,
    interest_tags: list[str],
    colors: BusinessCardColors,
):
    draw = ImageDraw.Draw(img)

    # サイズ計算
    label_rect = get_label_rect(img)

    summary_container_w = (img.width - label_rect.w) / 2
    summary_container_h: int = img.height

    summary_w = (img.width - label_rect.w) / 2 - 25 * 2

    icon_w, icon_h = (120, 120)

    ICON_NAME_GAP = 20
    name_w = summary_w - icon_w - ICON_NAME_GAP
    _, _, _, name_h = textbbox_with_wrap(
        draw,
        xy=(0, 0),
        width=name_w,
        text=username,
        font=NAME_FONT,
    )

    rank_w = name_w
    if rank is not None:
        _, _, _, rank_h = textbbox_with_wrap(
            draw,
            xy=(0, 0),
            width=rank_w,
            text=rank,
            font=RANK_FONT,
            stroke_width=3,
        )
    else:
        rank_h = 0

    tags_w = summary_w
    if interest_tags is not None:
        tags_h = tagsbox(
            draw=draw,
            tags=interest_tags,
            font=FONT,
            width=summary_w,
        ).h
    else:
        tags_h = 0

    NAME_RANK_GAP = 20
    RANK_TAG_GAP = 30

    summary_h = (
        max(
            icon_h,
            name_h + NAME_RANK_GAP + rank_h,
        )
        + RANK_TAG_GAP
        + tags_h
    )

    # 位置計算
    summary_x = summary_container_w / 2 - summary_w / 2
    summary_y = summary_container_h / 2 - summary_h / 2

    icon_x, icon_y = summary_x, summary_y

    name_x = icon_x + icon_w + ICON_NAME_GAP
    name_y = summary_y

    rank_x = name_x
    rank_y = name_y + name_h + NAME_RANK_GAP

    tags_x = summary_x
    tags_y = (
        summary_y
        + max(
            icon_h,
            name_h + NAME_RANK_GAP + rank_h,
        )
        + RANK_TAG_GAP
    )

    # 描画
    icon_img = Image.open(icon).resize((icon_w, icon_h))
    img.paste(icon_img, box=(int(icon_x), int(icon_y)))
    # img.alpha_composite(icon_img, dest=(int(icon_x), int(icon_y)))

    draw_text(
        img,
        xy=(name_x, name_y),
        width=name_w,
        text=username,
        font=NAME_FONT,
        stroke_fill=colors.text.edge,
        stroke_width=3,
        fill=colors.text.inner,
    )

    if rank is not None:
        draw_text(
            img,
            xy=(rank_x, rank_y),
            width=rank_w,
            text=rank,
            font=RANK_FONT,
            stroke_fill=colors.text.edge,
            stroke_width=3,
            fill=colors.text.inner,
        )

    if interest_tags is not None:
        draw_tags(
            img=img,
            tags=interest_tags,
            font=FONT,
            colors=colors.label,
            xy=(tags_x, tags_y),
            width=tags_w,
        )


def _draw_arts(img: Image.Image, arts, colors):
    draw = ImageDraw.Draw(img)

    label_rect = get_label_rect(img)

    rect1 = Rect.new_ltwh(
        label_rect.right,
        img.height / 3 * 0,
        img.width - label_rect.right - 1,
        img.height / 3 - 1,
    )
    rect2 = Rect.new_ltwh(
        label_rect.right,
        img.height / 3 * 1,
        img.width - label_rect.right - 1,
        img.height / 3 - 1,
    )
    rect3 = Rect.new_ltwh(
        label_rect.right,
        img.height / 3 * 2,
        img.width - label_rect.right - 1,
        img.height / 3 - 1,
    )

    rect1_img = Image.new("RGBA", img.size)
    rect1_draw = ImageDraw.Draw(rect1_img)
    rect1_draw.rectangle(rect1.to_tuple(), colors.arts[0].box)
    img.alpha_composite(rect1_img)

    rect2_img = Image.new("RGBA", img.size)
    rect2_draw = ImageDraw.Draw(rect2_img)
    rect2_draw.rectangle(rect2.to_tuple(), colors.arts[1].box)
    img.alpha_composite(rect2_img)

    rect3_img = Image.new("RGBA", img.size)
    rect3_draw = ImageDraw.Draw(rect3_img)
    rect3_draw.rectangle(rect3.to_tuple(), colors.arts[2].box)
    img.alpha_composite(rect3_img)

    # 文字入れ１

    rec1_inner_rect = rect1.inner_rect(padding=Padding.new_all(34))
    draw.text(rec1_inner_rect.offset.to_tuple(), arts[0], font=get_font(35))

    # 文字入れ２
    rec2_inner_rect = rect2.inner_rect(padding=Padding.new_all(34))
    draw.text(rec2_inner_rect.offset.to_tuple(), arts[1], font=get_font(35))

    # 文字入れ３
    rec3_inner_rect = rect3.inner_rect(padding=Padding.new_all(34))
    draw.text(rec3_inner_rect.offset.to_tuple(), arts[2], font=get_font(35))


def businesscard_type_1(
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

    _draw_label(img, colors[theme_color].label)
    _draw_summary(img, icon, username, rank,
                  interest_tags, colors[theme_color])
    _draw_arts(img, arts, colors[theme_color])

    # img.save("output.png")
    return img


# businesscard_type_1(
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

if __name__ == "__main__":
    businesscard_type_1(
        "つーばーさ",
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
    ).save("./output.png")
