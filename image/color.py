from image.type import Number


class Color:
    def __init__(self, r: Number, g: Number, b: Number, a: Number) -> None:
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    @property
    def r(self):
        return int(self._r)

    @property
    def g(self):
        return int(self._g)

    @property
    def b(self):
        return int(self._b)

    @property
    def a(self):
        return int(self._a)

    @staticmethod
    def new_rgba(r: Number, g: Number, b: Number, a: Number = 255):
        return Color(r, g, b, a)

    @staticmethod
    def new_hex(hex: str):
        hex = hex.lstrip("#")
        if len(hex) == 6:
            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
            return Color.new_rgba(r, g, b)
        elif len(hex) == 8:
            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
            a = int(hex[6:8], 16)
            return Color.new_rgba(r, g, b, a)
