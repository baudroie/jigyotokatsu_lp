"""Build QA previews only. Source career assets are never modified."""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
source = root / "新素材" / "キャリア"
items = [
    ("PC01", source / "PC" / "pc_01_year1_candidate.png"),
    ("PC02", source / "PC" / "pc_02_year2-3_advisor.png"),
    ("PC03", source / "PC" / "pc_03_year4-5_business-head.png"),
    ("PC04", source / "PC" / "pc_04_year6-plus_president.png"),
    ("SP01", source / "SP" / "sp_01_year1_candidate.png"),
    ("SP02", source / "SP" / "sp_02_year2-3_advisor.png"),
    ("SP03", source / "SP" / "sp_03_year4-5_business-head.png"),
    ("SP04", source / "SP" / "sp_04_year6-plus_president.png"),
]
cell_w, cell_h, label_h = 320, 500, 26
sheet = Image.new("RGB", (cell_w * 4, cell_h * 2), "#eeeeee")
draw = ImageDraw.Draw(sheet)
for index, (label, path) in enumerate(items):
    image = Image.open(path).convert("RGBA")
    image.thumbnail((cell_w - 12, cell_h - label_h - 12), Image.Resampling.LANCZOS)
    x0, y0 = (index % 4) * cell_w, (index // 4) * cell_h
    x = x0 + (cell_w - image.width) // 2
    y = y0 + label_h + (cell_h - label_h - image.height) // 2
    background = Image.new("RGBA", image.size, "white")
    background.alpha_composite(image)
    sheet.paste(background.convert("RGB"), (x, y))
    draw.text((x0 + 8, y0 + 7), label, fill="black")
sheet.save(Path(__file__).with_name("source-contact-sheet.jpg"), quality=94)
