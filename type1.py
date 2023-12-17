from PIL import Image, ImageDraw

from colors import colors
from image.cut import cut_circle
from image.flow_layout import textbbox_with_wrap
from image.layout import Offset, Padding, Rect, Size
from image.shadow import draw_text_with_shadow
from image.text import draw_text
from settings import get_font
from tag import draw_tag, tag_bbox

FONT = get_font(32)

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


def _draw_summary(img: Image.Image, icon, username, rank, interest_tags, colors):
    draw = ImageDraw.Draw(img)

    # サイズの計算

    container_padding_x = 28

    container_w = (
        img.width
        - get_label_rect(img).right
        - container_padding_x
        - container_padding_x
    )

    # アイコンのサイズ
    icon_w, icon_h = (120, 120)

    # 名前のサイズ
    USERNAME_FONT = get_font(64)
    _, _, username_w, username_h = textbbox_with_wrap(
        draw,
        (0, 0),
        text=username,
        width=container_w - icon_w - 40,
        font=USERNAME_FONT,
    )

    # 称号のサイズ
    RANK_FONT = get_font(48)
    _, _, rank_w, rank_h = textbbox_with_wrap(
        draw,
        (0, 0),
        text=rank,
        width=container_w - icon_w - 40,
        font=RANK_FONT,
    )

    # タグのサイズ
    tag_start_x = 0
    tag_start_y = 0
    tag_current_x = tag_start_x
    tag_current_y = tag_start_y
    tag_max_h = 0

    TAG_H_GAP = 9
    TAG_V_GAP = 9

    for tag in interest_tags:
        tag_w, tag_h = tag_bbox(draw, tag)
        if tag_current_x + tag_w < tag_start_x + container_w:
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

    tags_w = container_w
    tags_h = tag_current_y + tag_max_h

    container_h = max(icon_h, username_h + rank_h) + 20 + tags_h

    container_x = container_padding_x
    container_y = (img.height - container_h) / 2

    # 描画
    # アイコンを描画
    icon_img = Image.open(icon)
    icon_img = icon_img.resize((icon_w, icon_h))
    icon_img = cut_circle(icon_img)
    img.alpha_composite(icon_img, dest=(int(container_x), int(container_y + 40)))

    # 名前を描画
    draw_text_with_shadow(
        img=img,
        xy=(container_x + icon_w + 40, container_y),
        text=username,
        width=container_w - icon_w - 40,
        fill=colors.text.inner,
        stroke_width=3,
        stroke_fill=colors.text.edge,
        font=USERNAME_FONT,
        shadow_radius=4,
        shadow_color=(0, 0, 0, int(255 * 0.25)),
        shadow_y=4,
    )

    # 称号を描画
    draw_text_with_shadow(
        img=img,
        xy=(container_x + icon_w + 40, container_y + username_h),
        text=rank,
        width=container_w - icon_w - 40,
        fill=colors.text.inner,
        stroke_width=1,
        stroke_fill=colors.text.edge,
        font=RANK_FONT,
        shadow_radius=4,
        shadow_color=(0, 0, 0, int(255 * 0.25)),
        shadow_y=4,
    )

    # タグ
    tag_start_x = container_x
    tag_start_y = container_y + username_h + rank_h + 20
    tag_current_x = tag_start_x
    tag_current_y = tag_start_y
    tag_max_h = 0

    for tag in interest_tags:
        tag_w, tag_h = tag_bbox(draw, tag)
        print(tag, tag_current_x, tag_w, container_w)
        if tag_current_x + tag_w < container_x + container_w:
            draw_tag(
                draw,
                (
                    tag_current_x,
                    tag_current_y,
                    tag_current_x + tag_w,
                    tag_current_y + tag_h,
                ),
                tag,
                fill=colors.label.box,
                text=colors.label.text,
            )
            tag_current_x += tag_w
            tag_current_x += TAG_H_GAP
        else:
            tag_current_x = tag_start_x
            tag_current_y += tag_max_h
            tag_current_y += TAG_V_GAP
            draw_tag(
                draw,
                (
                    tag_current_x,
                    tag_current_y,
                    tag_current_x + tag_w,
                    tag_current_y + tag_h,
                ),
                tag,
                fill=colors.label.box,
                text=colors.label.text,
            )
            tag_max_h = tag_h
            tag_current_x += tag_w
            tag_current_x += TAG_H_GAP
        tag_max_h = tag_h if tag_h > tag_max_h else tag_max_h


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
    img = Image.open(background_image)

    _draw_label(img, colors[theme_color].label)
    _draw_summary(img, icon, username, rank, interest_tags, colors[theme_color])
    _draw_arts(img, arts, colors[theme_color])

    img.save("output.png")


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
