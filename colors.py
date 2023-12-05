WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class BusinessCardColors:
    def __init__(self, label, arts, text) -> None:
        self.label = label
        self.arts = arts
        self.text = text


class BoxColors:
    def __init__(self, box, text=WHITE) -> None:
        self.box = box
        self.text = text


class TextColors:
    def __init__(self, edge, inner=WHITE) -> None:
        self.inner = inner
        self.edge = edge


colors = {
    "red": BusinessCardColors(
        text=TextColors(
            edge=(182, 7, 7),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(255, 0, 0),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(255, 86, 86, int(255 * 0.75)),
                text=WHITE,
            ),
            BoxColors(
                box=(255, 120, 120, int(255 * 0.75)),
                text=WHITE,
            ),
            BoxColors(
                box=(255, 138, 138, int(255 * 0.75)),
                text=WHITE,
            ),
        ],
    ),
    "blue": BusinessCardColors(
        text=TextColors(
            edge=(11, 18, 186),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(0, 10, 255),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(65, 72, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(106, 112, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(151, 155, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "green": BusinessCardColors(
        text=TextColors(
            edge=(7, 193, 37),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(0, 255, 41),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(58, 255, 90, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(113, 255, 135, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(154, 255, 170, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "yellow": BusinessCardColors(
        text=TextColors(
            edge=(194, 198, 8),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(250, 255, 0),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(251, 255, 57, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(252, 255, 96, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(253, 253, 133, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "orange": BusinessCardColors(
        text=TextColors(
            edge=(193, 100, 14),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(255, 122, 0),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(255, 151, 55, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(254, 171, 95, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(255, 191, 133, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "purple": BusinessCardColors(
        text=TextColors(
            edge=(149, 10, 198),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(189, 0, 255),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(205, 63, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(213, 92, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(221, 124, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "pink": BusinessCardColors(
        text=TextColors(
            edge=(192, 14, 153),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(255, 0, 199),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(255, 49, 210, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(255, 80, 216, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(255, 121, 226, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "sky": BusinessCardColors(
        text=TextColors(
            edge=(15, 174, 195),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(0, 224, 255),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(43, 230, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(81, 234, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(132, 240, 255, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "brown": BusinessCardColors(
        text=TextColors(
            edge=(131, 67, 67),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(166, 73, 73),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(181, 96, 96, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(190, 120, 120, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(190, 136, 136, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "black": BusinessCardColors(
        text=TextColors(
            edge=(0, 0, 0),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(52, 52, 52),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(80, 79, 79, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(117, 117, 117, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(150, 150, 150, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "yellow-green": BusinessCardColors(
        text=TextColors(
            edge=(112, 185, 18),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(143, 255, 0),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(171, 255, 63, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(186, 255, 98, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(203, 255, 137, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
    "white": BusinessCardColors(
        text=TextColors(
            edge=(255, 255, 255),
            inner=WHITE,
        ),
        label=BoxColors(
            box=(238, 238, 238),
            text=WHITE,
        ),
        arts=[
            BoxColors(
                box=(224, 224, 224, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(208, 208, 208, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
            BoxColors(
                box=(188, 188, 188, int(255 * 0.75)),
                text=(0, 0, 0),
            ),
        ],
    ),
}
