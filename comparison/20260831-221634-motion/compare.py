"""Diagnostic outputs only; never writes to original assets or references."""
from pathlib import Path
from PIL import Image, ImageChops
import json

folder = Path(__file__).resolve().parent
root = folder.parents[1]
reports = []
for width, name, reference in [(1440, 'desktop', 'デザイン案web.png'), (390, 'mobile', 'デザイン案mobile.png'), (375, 'small-mobile', 'デザイン案mobile.png')]:
    before = Image.open(folder / f'before-{width}.png').convert('RGB')
    after = Image.open(folder / f'after-{width}.png').convert('RGB')
    assert before.size == after.size
    pair = Image.new('RGB', (width * 2, before.height), 'white')
    pair.paste(before); pair.paste(after, (width, 0))
    pair.save(folder / f'{name}-before-after.png')
    Image.blend(before, after, .5).save(folder / f'{name}-overlay.png')
    diff = ImageChops.difference(before, after)
    diff.save(folder / f'{name}-diff.png')
    reports.append({'width': width, 'size': before.size, 'changedPixelBoundingBox': diff.getbbox()})
    ref = Image.open(root / reference).convert('RGB')
    ref = ref.resize((width, round(ref.height * width / ref.width)), Image.Resampling.LANCZOS)
    combined = Image.new('RGB', (width * 3, max(ref.height, after.height)), 'white')
    combined.paste(ref); combined.paste(before, (width, 0)); combined.paste(after, (width * 2, 0))
    combined.save(folder / f'{name}-reference-before-after.png')
    # Compact people crops: enough context to inspect both requested controls.
    metrics = json.loads((folder / 'after-metrics.json').read_text())
    record = next(m for m in metrics if m['width'] == width)
    people = next(s for s in record['sections'] if s['name'].startswith('people'))
    y = round(people['top'])
    pair.crop((0, y, width * 2, round(y + people['height']))).save(folder / f'{name}-people-comparison.png')
(folder / 'pixel-comparison.json').write_text(json.dumps(reports, indent=2))
print(json.dumps(reports, indent=2))
