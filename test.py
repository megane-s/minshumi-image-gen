from PIL import Image, ImageDraw
from image.layout import Rect, row_size, Offset

img = Image.new("RGBA", (1200, 1200))
draw = ImageDraw.Draw(img)


rect1 = Rect.new_ltwh(10, 10, 100, 100)
rect2 = Rect.new_ltwh(10, 10, 100, 100)
rect3 = Rect.new_ltwh(10, 10, 100, 100)

size_total = row_size(rect1.size, rect2.size, rect3.size)
rect_total = Rect.new_offset_size(Offset.new_xy(0, 0), size_total)

draw.rectangle(rect_total.to_tuple(), outline=(255, 0, 0))
# draw.rectangle(rect.to_tuple(), (255, 0, 0))

img.save("output.png")
