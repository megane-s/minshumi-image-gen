
from regression_test.test_data import test_data
from type2 import businesscard_type_2


def test_type2():
    for key, data in test_data.items():
        businesscard_type_2(
            username=data["username"],
            icon=data["icon"],
            rank=data["rank"],
            interest_tags=data["interest_tags"],
            arts=data["arts"],
            background_image=data["background_image"],
            theme_color=data["theme_color"],
        ).save(f"./regression_test/output/type-2-{key}.png")
