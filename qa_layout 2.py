"""Read-only asset analysis and reproducible layout reports (never modifies sources)."""
import json
from pathlib import Path
import sys
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent
REFERENCE = {
    'desktop': {'width': 661, 'hero': (0,388), 'benefits': (362,535),
                'frontline': (535,808), 'field': (808,1008), 'career': (1008,1237),
                'people': (1237,1453), 'flow': (1453,1603), 'final-cta': (1603,1736),
                'site-footer': (1736,1804)},
    'mobile': {'width': 183, 'hero': (0,328), 'benefits': (328,618),
               'frontline': (618,858), 'career': (858,1199), 'people': (1199,1353),
               'flow': (1353,1545), 'final-cta': (1545,1674), 'site-footer': (1674,1793)}
}

def report(label):
    folder = ROOT / 'comparison' / label
    audit = json.loads((folder / 'audit.json').read_text())
    metrics, images = {}, {}
    lines = [f'## {label}', '', 'Reference is LEFT; coordinates are CSS px after width-only scaling.',
             'Reference section boundaries were measured manually (±2 source pixels). No vertical stretching.', '']
    for name, data in audit.items():
        metrics[name] = {'viewport': data['viewport'], 'sections': {}}
        for item in data['images']:
            if not item['naturalWidth'] or not item['visible']:
                continue
            bitmap = Image.open(ROOT / item['src']).convert('RGBA')
            bbox = bitmap.getchannel('A').point(lambda a: 255 if a > 128 else 0).getbbox()
            item['foregroundBoundsAlpha128'] = bbox
            item['naturalAspectRatio'] = item['naturalWidth'] / item['naturalHeight']
            item['renderedAspectRatio'] = item['rendered']['width'] / item['rendered']['height']
            item['ratioPreserved'] = abs(item['naturalAspectRatio']-item['renderedAspectRatio']) < .002
            item['compositeSource'] = item['src'] == 'assets/cards/cards-strip.png'
        visible = [i for i in data['images'] if i['visible']]
        clipped_images = [i for i in visible if i['clippedBy']]
        images[name] = {'viewport': data['viewport'], 'summary': {
            'visibleImages': len(visible),
            'clippingCandidates': len(clipped_images),
            'nonCompositeClippingCandidates': len([i for i in clipped_images if not i.get('compositeSource')]),
            'distortedImages': len([i for i in visible if i.get('ratioPreserved') is False]),
            'pageHasHorizontalOverflow': data['viewport']['scrollWidth'] > data['viewport']['clientWidth'],
            'note': 'Benefits uses an existing composite viewport; it is NOT claimed to be a full uncut PNG. Alpha128 bounds are diagnostic, not a mask.'
        }, 'images': data['images']}
        if name not in REFERENCE:
            continue
        ref = REFERENCE[name]
        scale = data['viewport']['width'] / ref['width']
        lines += [f'### {name}', '', '| Section | Ref start | Ref end | Ref height | Current start | Current end | Current height | Δstart | Δend |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for section in ref:
            if section == 'width': continue
            box = data['sections'][section]
            a,b = [v*scale for v in ref[section]]
            current = {k: round(box[k],2) for k in ['top','bottom','height']}
            metrics[name]['sections'][section] = {'reference': {'top':a,'bottom':b,'height':b-a}, 'current':current, 'deltaTop':current['top']-a,'deltaBottom':current['bottom']-b}
            values = [a,b,b-a,current['top'],current['bottom'],current['height'],current['top']-a,current['bottom']-b]
            lines.append('| '+section+' | '+' | '.join(f'{v:.1f}' for v in values)+' |')
        clipped = [i for i in data['images'] if i['visible'] and i['clippedBy']]
        lines += ['', f'Bounding-box clipping candidates: {len(clipped)}. This is a geometric test; transparent gutters are not equivalent to clipped text.', '']
        # Focused comparisons preserve image aspect ratio and align section starts only.
        source = Image.open(next(ROOT.glob('*案'+('web' if name=='desktop' else 'mobile')+'.png'))).convert('RGB')
        shot = Image.open(folder / f"{name}-{data['viewport']['width']}.png").convert('RGB')
        shot = shot.resize((source.width, round(shot.height*source.width/shot.width)), Image.Resampling.LANCZOS)
        for section in ['hero','benefits','career','people','final-cta']:
            ra,rb=ref[section]; box=data['sections'][section]
            ca,cb=round(box['top']/scale),round(box['bottom']/scale)
            pair=Image.new('RGB',(source.width*2,max(rb-ra,cb-ca)), 'white')
            pair.paste(source.crop((0,ra,source.width,rb)),(0,0))
            pair.paste(shot.crop((0,ca,source.width,cb)),(source.width,0))
            pair.save(folder / f'{name}-{section}-focused.png')
    (folder / 'layout-metrics.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False))
    (folder / 'image-layout-audit.json').write_text(json.dumps(images,indent=2,ensure_ascii=False))
    (folder / 'metrics.md').write_text('\n'.join(lines)+'\n')
    (ROOT / 'layout-metrics.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False))
    (ROOT / 'image-layout-audit.json').write_text(json.dumps(images,indent=2,ensure_ascii=False))
    print('\n'.join(lines))

if __name__ == '__main__':
    report(sys.argv[1])
