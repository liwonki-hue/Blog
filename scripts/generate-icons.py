from PIL import Image, ImageDraw, ImageFont
import os

BG_COLOR = (30, 30, 30, 255)
FG_COLOR = (255, 255, 255, 255)
LETTER = "M"
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(OUT_DIR, exist_ok=True)


def make_icon(size, corner_radius_ratio=0.0):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if corner_radius_ratio > 0:
        draw.rounded_rectangle(
            [(0, 0), (size - 1, size - 1)],
            radius=int(size * corner_radius_ratio),
            fill=BG_COLOR,
        )
    else:
        draw.rectangle([(0, 0), (size - 1, size - 1)], fill=BG_COLOR)

    font_size = int(size * 0.6)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), LETTER, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos = ((size - text_w) / 2 - bbox[0], (size - text_h) / 2 - bbox[1])
    draw.text(pos, LETTER, font=font, fill=FG_COLOR)
    return img


sizes = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512,
}

images = {}
for name, size in sizes.items():
    radius_ratio = 0.18 if name == "apple-touch-icon.png" else 0.0
    img = make_icon(size, radius_ratio)
    img.save(os.path.join(OUT_DIR, name))
    images[size] = img
    print(f"wrote {name} ({size}x{size})")

# favicon.ico: multi-resolution
ico_path = os.path.join(OUT_DIR, "favicon.ico")
base = make_icon(48)
base.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon.ico (16/32/48)")

# safari-pinned-tab.svg: simple monochrome mask icon (black shape, transparent bg)
svg_path = os.path.join(OUT_DIR, "safari-pinned-tab.svg")
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
<path d="M3 2h1.6L8 8.2 11.4 2H13v12h-1.7V5.1L8.4 11h-0.8L4.7 5.1V14H3V2z"/>
</svg>
"""
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print("wrote safari-pinned-tab.svg")

print("done")
