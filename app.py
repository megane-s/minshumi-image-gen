import io

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, send_file

from image.download import clear_image_cache, get_local_path
from type1 import businesscard_type_1
from type2 import businesscard_type_2
from type3 import businesscard_type_3
from util.env import get_env_with_default

app = Flask(__name__)


@app.route("/test")
def test_page():
    return render_template("index.html")


@app.route("/gen")
def gen_image():
    card_type = request.args.get("type", default="1")
    username = get_username()
    icon = get_icon()
    rank = get_rank()
    interest_tags = get_interest_tags()
    arts = get_arts()
    background_image = get_background_image()
    theme_color = get_theme_color()
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
    else:
        return "not found", 404

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/png")


def get_username():
    username = request.args.get("username", default=None)
    if username is None:
        raise NotImplementedError(f"invalid username : {username}")
    return username


def get_icon():
    return request.args.get(
        "icon",
        default="https://storage.googleapis.com/minshumi-user-content/logo-square-1080x1080.png",
    )


def get_rank():
    rank = request.args.get("rank", default="")  # None にしたい
    if len(rank) == 0:
        rank = None
    return rank


def get_interest_tags():
    tags = request.args.get("interest_tags", default=None)
    if tags is None or len(tags) == 0:
        return None
    return tags.split(",")


def get_arts():
    arts = request.args.get("arts", default=None)
    if arts is None:
        arts = ""
    arts = arts.split(",")
    if len(arts) != 3:
        for i in range(3):
            if len(arts) <= i:
                arts.append("")
    return arts


def get_background_image():
    return request.args.get(
        "background_image",
        default="https://storage.googleapis.com/minshumi-user-content/logo-rect-1200x675.png",
    )


def get_theme_color():
    return request.args.get(
        "theme_color",
        default="red",
    )


def setup_startup_jobs():
    # スケジューラのインスタンスを作成する
    scheduler = BackgroundScheduler()
    # スケジューラーにジョブを追加する
    interval_min = int(get_env_with_default(
        "AUTO_CLEAR_CACHE_INTERVAL_MIN", "30")
    )
    scheduler.add_job(clear_image_cache, "interval", minutes=interval_min)
    # スケジューラを開始する
    scheduler.start()


setup_startup_jobs()
