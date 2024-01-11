import io

from flask import Flask, render_template, request, send_file

from image.download import get_local_path
from type1 import businesscard_type_1
from type2 import businesscard_type_2
from type3 import businesscard_type_3
from type4 import businesscard_type_4

from upload_image.router import upload_user_content

app = Flask(__name__)
app.register_blueprint(upload_user_content)


@app.route("/test")
def test_page():
    return render_template("index.html")


@app.route("/gen")
def gen_image():
    card_type = request.args.get("type", default="1")
    # username = "つーばーさつーばーさ"
    # icon = "./placeholder/400x400_green.png"
    # rank = "アクションマスター"
    # interest_tags = ["アクション","SF","恋愛","アニメ"]
    # arts = ["ずっと真夜中でいいのに。", "かいけつゾロリ", "呪術廻戦"]
    # background_image = "./placeholder/1200x675_red.png"
    # theme_color = "red"
    username = request.args.get("username")
    icon = request.args.get("icon")
    rank = request.args.get("rank")
    interest_tags = request.args.get("interest_tags", default="").split(",")
    arts = request.args.get("arts", default="").split(",")
    background_image = request.args.get("background_image")
    theme_color = request.args.get("theme_color")
    if not any(
        [username, icon, rank, interest_tags, arts, background_image, theme_color]
    ):
        return "invalid args", 400
    icon = get_local_path(icon)
    background_image = get_local_path(background_image)

    if card_type == "1":
        img = businesscard_type_1(
            username=username,
            icon=icon,
            rank=rank,
            interest_tags=interest_tags,
            arts=arts,
            background_image=background_image,
            theme_color=theme_color,
        )
    elif card_type == "2":
        img = businesscard_type_2(
            username=username,
            icon=icon,
            rank=rank,
            interest_tags=interest_tags,
            arts=arts,
            background_image=background_image,
            theme_color=theme_color,
        )
    elif card_type == "3":
        img = businesscard_type_3(
            username=username,
            icon=icon,
            rank=rank,
            interest_tags=interest_tags,
            arts=arts,
            background_image=background_image,
            theme_color=theme_color,
        )
    elif card_type == "4":
        img = businesscard_type_4(
            username=username,
            icon=icon,
            rank=rank,
            interest_tags=interest_tags,
            arts=arts,
            background_image=background_image,
            theme_color=theme_color,
        )
    else:
        return "not found", 404

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/png")
