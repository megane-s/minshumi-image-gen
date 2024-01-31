
from colors import colors

test_data = {}

for color in colors.keys():
    test_data[f"{color}"] = {
        "username": "つーばーさ",
        "icon": "./placeholder/400x400_green.png",
        "rank": "アクションマスター",
        "interest_tags": [
            "アクション",
            "SF",
            "恋愛",
            "アニメ",
            "SF",
            "恋愛",
            "SF",
        ],
        "arts": ["ずっと真夜中でいいのに。", "かいけつゾロリ", "呪術廻戦"],
        "background_image": "./placeholder/1200x675_red.png",
        "theme_color": color,
    }
