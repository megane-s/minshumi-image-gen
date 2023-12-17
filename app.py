from flask import Flask, request, send_file

from type1 import businesscard_type_1
from type2 import businesscard_type_2
from type3 import businesscard_type_3
from type4 import businesscard_type_4

app = Flask(__name__)


@app.route("/gen")
def type4():
    type = request.args.get("type", default="1")
    if type == "1":
            businesscard_type_1(
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
    elif type == "2":
            businesscard_type_2(
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
    elif type == "3":
            businesscard_type_3(
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
    elif type == "4":
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
    else:
        return "not found", 404

    return send_file("./output.png")
