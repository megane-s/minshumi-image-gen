from PIL import Image


class AlphaCompositeContext:
    def __init__(self, img: Image.Image) -> None:
        self.img = img

    def __enter__(self):
        self.overlay = Image.new("RGBA", self.img.size)
        return self.overlay

    def __exit__(self, ex_type, ex_value, trace):
        self.img = self.img.alpha_composite(self.overlay)
