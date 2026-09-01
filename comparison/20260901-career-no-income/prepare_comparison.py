"""Create focused QA comparisons without changing any source or site asset."""
from pathlib import Path
from PIL import Image
import hashlib, json

folder = Path(__file__).resolve().parent
root = folder.parents[1]
paths = {
    "pc": [root / "新素材/キャリア/PC" / f for f in [
        "pc_01_year1_candidate.png", "pc_02_year2-3_advisor.png",
        "pc_03_year4-5_business-head.png", "pc_04_year6-plus_president.png"]],
    "sp": [root / "新素材/キャリア/SP" / f for f in [
        "sp_01_year1_candidate.png", "sp_02_year2-3_advisor.png",
        "sp_03_year4-5_business-head.png", "sp_04_year6-plus_president.png"]],
}

manifest = []
for kind, files in paths.items():
    for source in files:
        placed = root / "assets/career/no-income-20260901" / source.name
        image = Image.open(source)
        manifest.append({
            "kind": kind.upper(), "source": str(source.relative_to(root)),
            "placed": str(placed.relative_to(root)), "size": list(image.size),
            "mode": image.mode, "alphaBounds": list(image.getbbox()),
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "copyIdentical": source.read_bytes() == placed.read_bytes(),
        })
(folder / "asset-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

def flatten(source, size):
    image = Image.open(source).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    base = Image.new("RGBA", size, "white")
    base.alpha_composite(image)
    return base.convert("RGB")

# PC: compare only the exact four-card row at its rendered width.
pc_impl = Image.open(folder / "after-raw-1440-final.png").convert("RGB").crop((0, 2222, 1440, 2438))
pc_src = Image.new("RGB", pc_impl.size, "white")
for i, source in enumerate(paths["pc"]):
    left = round(50 + i * 336.25)
    right = round(50 + i * 336.25 + 331.25)
    pc_src.paste(flatten(source, (right-left, 215)), (left, 0))
pc_pair = Image.new("RGB", (2880, 216), "white")
pc_pair.paste(pc_src); pc_pair.paste(pc_impl, (1440, 0))
pc_pair.save(folder / "desktop-source-implementation.png")

# SP focused comparison: same first-card state from the viewport screenshot.
# The separate contact sheet above remains the all-four asset inventory.
sp_impl = Image.open(folder / "after-raw-390-final.png").convert("RGB").crop((0, 3136, 390, 3671))
sp_src = Image.new("RGB", sp_impl.size, "white")
sp_src.paste(flatten(paths["sp"][0], (348, 535)), (21, 0))
sp_pair = Image.new("RGB", (780, 535), "white")
sp_pair.paste(sp_src); sp_pair.paste(sp_impl, (390, 0))
sp_pair.save(folder / "mobile-source-implementation.png")
