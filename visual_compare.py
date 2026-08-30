#!/usr/bin/env python3
"""Create normalized side-by-side, overlay, and diff images for visual QA."""

import json
from pathlib import Path
import sys

from PIL import Image, ImageChops


def compare(loop_name: str) -> None:
    root = Path(__file__).resolve().parent
    output = root / "comparison" / loop_name
    pairs = (
        ("desktop", root / "デザイン案web.png", output / "desktop-1440.png"),
        ("mobile", root / "デザイン案mobile.png", output / "mobile-390.png"),
    )

    for name, reference_path, implementation_path in pairs:
        reference = Image.open(reference_path).convert("RGB")
        implementation = Image.open(implementation_path).convert("RGB")
        normalized_height = round(
            implementation.height * reference.width / implementation.width
        )
        implementation = implementation.resize(
            (reference.width, normalized_height), Image.Resampling.LANCZOS
        )

        height = max(reference.height, implementation.height)
        reference_normalized = Image.new("RGB", (reference.width, height), "white")
        implementation_normalized = Image.new("RGB", (reference.width, height), "white")
        reference_normalized.paste(reference, (0, 0))
        implementation_normalized.paste(implementation, (0, 0))

        side_by_side = Image.new("RGB", (reference.width * 2, height), "white")
        side_by_side.paste(reference_normalized, (0, 0))
        side_by_side.paste(implementation_normalized, (reference.width, 0))
        side_by_side.save(output / f"{name}-side-by-side.png")

        Image.blend(reference_normalized, implementation_normalized, 0.5).save(
            output / f"{name}-overlay.png"
        )
        ImageChops.difference(reference_normalized, implementation_normalized).save(
            output / f"{name}-diff.png"
        )

        print(
            f"{name}: reference={reference.size}, "
            f"implementation={implementation.size}"
        )


def stitch(loop_name: str) -> None:
    root = Path(__file__).resolve().parent
    output = root / "comparison" / loop_name
    for label in ("desktop-1440", "mobile-390"):
        manifest = json.loads((output / f"{label}-manifest.json").read_text())
        canvas = Image.new(
            "RGB", (manifest["width"], manifest["scrollHeight"]), "white"
        )
        for part in sorted(manifest["parts"], key=lambda item: item["y"]):
            image = Image.open(output / part["file"]).convert("RGB")
            remaining = manifest["scrollHeight"] - part["y"]
            if image.height > remaining:
                image = image.crop((0, 0, image.width, remaining))
            canvas.paste(image, (0, part["y"]))
        canvas.save(output / f"{label}.png")
        print(f"stitched {label}: {canvas.size}")


def focused(loop_name: str) -> None:
    root = Path(__file__).resolve().parent
    loop = root / "comparison" / loop_name
    output = root / "comparison"
    specs = {
        "desktop": {
            "reference": root / "デザイン案web.png",
            "implementation": loop / "desktop-1440.png",
            "regions": {"hero": (0, 0, 661, 536), "career": (0, 1000, 661, 1240), "final": (0, 1600, 661, 1804)},
        },
        "mobile": {
            "reference": root / "デザイン案mobile.png",
            "implementation": loop / "mobile-390.png",
            "regions": {"hero": (0, 0, 183, 620), "career": (0, 850, 183, 1200), "final": (0, 1540, 183, 1793)},
        },
    }
    for viewport, spec in specs.items():
        reference = Image.open(spec["reference"]).convert("RGB")
        implementation = Image.open(spec["implementation"]).convert("RGB")
        implementation = implementation.resize(
            (reference.width, reference.height), Image.Resampling.LANCZOS
        )
        for region, box in spec["regions"].items():
            ref_crop = reference.crop(box)
            imp_crop = implementation.crop(box)
            canvas = Image.new("RGB", (ref_crop.width * 2, ref_crop.height), "white")
            canvas.paste(ref_crop, (0, 0))
            canvas.paste(imp_crop, (ref_crop.width, 0))
            canvas.save(output / f"focused-{viewport}-{region}.png")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "stitch":
        stitch(sys.argv[2])
    elif len(sys.argv) > 2 and sys.argv[1] == "focus":
        focused(sys.argv[2])
    else:
        compare(sys.argv[1] if len(sys.argv) > 1 else "final")
