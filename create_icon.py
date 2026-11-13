from pathlib import Path

from PIL import Image

source = Path("app_icon.png")
output = Path("Quack.iconset")
output.mkdir(exist_ok=True)

image = Image.open(source).convert("RGBA")

sizes = [
    (16, "icon_16x16.png"),
    (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),
    (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),
    (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),
    (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),
    (1024, "icon_512x512@2x.png"),
]

for size, filename in sizes:
    resized = image.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(output / filename)

print("Iconset created.")
