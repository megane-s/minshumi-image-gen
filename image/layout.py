from image.type import Length


class Offset:
    def __init__(self, x: Length, y: Length):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return int(self._x)

    @property
    def y(self) -> int:
        return int(self._y)

    def to_tuple(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"Offset(x={self.x},y={self.y})"

    @staticmethod
    def new_xy(x: Length, y: Length):
        return Offset(x, y)


class Size:
    def __init__(self, w: Length, h: Length):
        self._w = w
        self._h = h

    @property
    def w(self) -> int:
        return int(self._w)

    @property
    def h(self) -> int:
        return int(self._h)

    def to_tuple(self) -> tuple[int, int]:
        return (self.w, self.h)

    def __str__(self) -> str:
        return f"Size(w={self.w},h={self.h})"

    @staticmethod
    def new_wh(w: Length, h: Length):
        return Size(w, h)


class Padding:
    def __init__(
        self,
        left: Length,
        top: Length,
        right: Length,
        bottom: Length,
    ) -> None:
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    @property
    def left(self):
        return int(self._left)

    @property
    def top(self):
        return int(self._top)

    @property
    def right(self):
        return int(self._right)

    @property
    def bottom(self):
        return int(self._bottom)

    def __str__(self) -> str:
        return f"Padding(left={self.left},top={self.top},right={self.right},bottom={self.bottom})"

    @staticmethod
    def new_all(padding: Length):
        return Padding(
            padding,
            padding,
            padding,
            padding,
        )

    @staticmethod
    def new_vh(vertical: Length = 0, horizontal: Length = 0):
        return Padding(
            top=vertical,
            bottom=vertical,
            left=horizontal,
            right=horizontal,
        )

    @staticmethod
    def new_ltrb(
        left: Length,
        top: Length,
        right: Length,
        bottom: Length,
    ):
        return Padding(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )


class Rect:
    def __init__(self, offset: Offset, size: Size) -> None:
        self._offset = offset
        self._size = size

    @property
    def offset(self):
        return self._offset

    @property
    def size(self):
        return self._size

    @property
    def l(self) -> int:
        return self.offset.x

    @property
    def left(self) -> int:
        return self.l

    @property
    def t(self) -> int:
        return self.offset.y

    @property
    def top(self) -> int:
        return self.t

    @property
    def r(self) -> int:
        return int(self.offset._x + self.size._w)

    @property
    def right(self) -> int:
        return self.r

    @property
    def b(self) -> int:
        return int(self.offset._y + self.size._h)

    @property
    def bottom(self) -> int:
        return self.b

    @property
    def w(self) -> int:
        return self.offset.w

    @property
    def width(self) -> int:
        return self.w

    @property
    def h(self) -> int:
        return self.offset.h

    @property
    def height(self) -> int:
        return self.h

    @property
    def ltrb(self):
        return (
            self.t,
            self.l,
            self.r,
            self.b,
        )

    @property
    def center(self):
        return Offset(self.l, self.t)

    def __str__(self) -> str:
        return f"Rect(t={self.t},l={self.l},r={self.r},b={self.b})"

    def inner_rect(self, padding=Padding.new_all(0)):
        return Rect.new_ltwh(
            left=self.l + padding.left,
            top=self.t + padding.top,
            w=self.w - padding.left - padding.right,
            h=self.h - padding.top - padding.bottom,
        )

    @staticmethod
    def new_ltrb(left: Length, top: Length, right: Length, bottom: Length):
        return Rect(
            Offset(left, top),
            Size(right - left, bottom - top),
        )

    @staticmethod
    def new_ltwh(left: Length, top: Length, w: Length, h: Length):
        return Rect(
            Offset(left, top),
            Size(w, h),
        )

    @staticmethod
    def new_offset_size(offset: Offset, size: Size):
        return Rect(offset, size)

    @staticmethod
    def new_center_wh(x: Length, y: Length, w: Length, h: Length):
        return Rect(
            Offset(x - w / 2, y - h / 2),
            Size(w, h),
        )


def column_size(*content_rects: Rect):
    w = 0
    h = 0
    for content in content_rects:
        w = content.w if content.w > w else w
        h += content.h
    return Size.new_wh(w, h)


def row_size(*content_rects: Rect):
    w = 0
    h = 0
    for content in content_rects:
        w += content.w
        h = content.h if content.h > h else h
    return Size.new_wh(w, h)
