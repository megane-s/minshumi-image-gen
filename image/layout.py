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
    def t(self) -> int:
        return self.offset.y

    @property
    def r(self) -> int:
        return int(self.offset._x + self.size._w)

    @property
    def b(self) -> int:
        return int(self.offset._y + self.size._h)

    @property
    def w(self) -> int:
        return self.offset.w

    @property
    def h(self) -> int:
        return self.offset.h

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
