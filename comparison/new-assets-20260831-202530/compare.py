"""Generate QA only; never overwrite reference/source PNGs or prior QA runs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, sys

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[1]
REF={
 'desktop':{'hero':[0,388],'benefits':[362,535],'frontline':[535,808],'field':[808,1008],'career':[1008,1237],'people':[1237,1453],'flow':[1453,1603],'final-cta':[1603,1736],'site-footer':[1736,1804]},
 'mobile':{'hero':[0,354],'benefits':[328,618],'frontline':[618,858],'career':[858,1199],'people':[1199,1353],'flow':[1353,1545],'final-cta':[1545,1674],'site-footer':[1674,1793]}
}
# Bounds describe visible card borders in the supplied low-resolution references.
CARDS={
 'desktop':{'benefits':[[28,363,231,515],[239,363,442,515],[450,363,637,515]],'career':[[28,1057,180,1193],[187,1057,339,1193],[346,1057,489,1193],[496,1057,637,1193]]},
 'mobile':{'benefits':[[6,328,176,418],[6,422,176,511],[6,515,176,604]],'career':[[7,898,172,956],[7,962,172,1020],[7,1027,172,1084],[7,1090,172,1147]]}
}
# Measured visible content envelope, not an invented CSS box in a raster image.
CONTENT={
 'desktop':{'hero':[16,7,653,346],'benefits':[28,363,637,515],'frontline':[119,554,532,779],'field':[5,819,651,1000],'career':[28,1020,637,1220],'people':[19,1237,645,1437],'flow':[28,1454,646,1577],'final-cta':[47,1637,634,1703],'site-footer':[20,1751,641,1786]},
 'mobile':{'hero':[10,18,173,310],'benefits':[6,328,176,604],'frontline':[8,636,172,839],'career':[7,875,172,1187],'people':[10,1213,172,1347],'flow':[10,1366,172,1535],'final-cta':[10,1563,172,1657],'site-footer':[11,1693,166,1770]}
}
def write(name,obj): (RUN/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def references():
    result={}
    for kind,width,pattern in [('desktop',1440,'*案web.png'),('mobile',390,'*案mobile.png')]:
        path=next(ROOT.glob(pattern));im=Image.open(path).convert('RGB');s=width/im.width
        result[kind]={'file':path.name,'size':im.size,'viewportWidth':width,'scale':s,'uncertaintyCssPx':2*s,'pageBounds':[0,0,im.width,im.height],'frameNote':'Use full canvas. Border/rounding about 1–2 source px included in measurement uncertainty; no screenshot was rescaled vertically.', 'sections':{},'cards':{}}
        result[kind]['pageBodyApprox']=[1,0,660,1803] if kind=='desktop' else [2,6,181,1792]
        result[kind]['frameNote']='Full reference canvas retained for consistent before/after comparison. Approximate page body recorded separately; SP has about 6 source px top white margin and 1–2 px side border. Coordinates start at the image top, not a cropped or vertically stretched page.'
        for name,(start,end) in REF[kind].items():
            b=CONTENT[kind][name]
            result[kind]['sections'][name]={'top':start*s,'bottom':end*s,'height':(end-start)*s,'sectionWidth':width,'containerWidth':(b[2]-b[0])*s,'visibleContentBounds':[v*s for v in b],'paddingTop':(b[1]-start)*s,'paddingBottom':(end-b[3])*s,'note':'Reference container/padding are visible raster envelopes/distances, not CSS declarations. Current container and CSS padding are recorded separately. Transparent gutters are not double-counted.'}
        for name,boxes in CARDS[kind].items():
            aspect=(.65 if kind=='mobile' else (1600/960 if name=='benefits' else 1600/1040))
            result[kind]['cards'][name]=[{'order':n+1,'sourceBounds':b,'width':(b[2]-b[0])*s,'height':(b[3]-b[1])*s,'sameWidthNewImageHeight':(b[2]-b[0])*s/aspect,'sameWidthHeightDelta':((b[2]-b[0])/aspect-(b[3]-b[1]))*s,'recommendedVisibleRatio':(b[2]-b[0])/(b[3]-b[1])} for n,b in enumerate(boxes)]
    pc=Image.open(next(ROOT.glob('*案web.png'))).convert('RGB');sp=Image.open(next(ROOT.glob('*案mobile.png'))).convert('RGB')
    result['backgroundSamples']={'desktop':[{ 'xy':p,'rgb':pc.getpixel(p)} for p in [(10,500),(330,525),(20,520),(5,530)]],'mobile':[{ 'xy':p,'rgb':sp.getpixel(p)} for p in [(3,340),(179,340),(3,480),(179,480),(4,611),(90,610),(90,616)]]}
    write('reference-metrics.json',result)
    return result

def compare(label):
    ref=references();metrics={};audits={}
    for kind,width in [('desktop',1440),('mobile',390)]:
        data=json.loads((RUN/label/f'{width}.json').read_text());current=Image.open(RUN/label/f'{width}.png').convert('RGB')
        target=Image.open(ROOT/ref[kind]['file']).convert('RGB')
        target=target.resize((width,round(target.height*width/target.width)),Image.Resampling.LANCZOS)
        assert current.width==width,(current.size,width)
        h=max(target.height,current.height)
        a=Image.new('RGB',(width,h),'#dedede');a.paste(target,(0,0));b=Image.new('RGB',(width,h),'#dedede');b.paste(current,(0,0))
        side=Image.new('RGB',(width*2,h));side.paste(a,(0,0));side.paste(b,(width,0));side.save(RUN/label/f'{kind}-side-by-side.png')
        Image.blend(a,b,.5).save(RUN/label/f'{kind}-overlay.png');ImageChops.difference(a,b).save(RUN/label/f'{kind}-diff.png')
        # Small review image also keeps both scales identical; no height fitting.
        side.resize((800,round(h*800/(width*2))),Image.Resampling.LANCZOS).save(RUN/label/f'{kind}-overview.jpg')
        metrics[kind]={}
        for name,r in ref[kind]['sections'].items():
            c=data['sections'][name]
            metrics[kind][name]={'reference':r,'current':c,'heightDelta':c['height']-r['height'],'cumulativeStartDelta':c['top']-r['top'],'endDelta':c['bottom']-r['bottom']}
            # Section-aligned comparison explicitly removes only upstream drift.
            ar=target.crop((0,round(r['top']),width,round(r['bottom'])));br=current.crop((0,round(c['top']),width,round(c['bottom'])))
            panel=Image.new('RGB',(width*2,max(ar.height,br.height)),'#dedede');panel.paste(ar,(0,0));panel.paste(br,(width,0))
            panel.resize((1000,round(panel.height*1000/panel.width)),Image.Resampling.LANCZOS).save(RUN/label/f'{kind}-{name}.jpg')
        for i in data['images']:
            p=ROOT/i['currentSrc'].split(':4173/')[-1]
            if p.is_file():
                im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox();i['alphaBounds']=box
                i['alphaBounds128']=im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                if box and i['naturalWidth'] and i['visible']:
                    s=i['width']/im.width
                    i['paintedBounds']={'left':i['left']+box[0]*s,'top':i['top']+box[1]*s,'width':(box[2]-box[0])*s,'height':(box[3]-box[1])*s}
        audits[kind]=data['images']
    (RUN/label/'layout-metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
    (RUN/label/'image-layout-audit.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2))
    rows=['Reference LEFT / Current RIGHT. Width-only scaling; gray = no page content.','']
    for kind,sections in metrics.items():
        rows+=['## '+kind,'','|Section|Ref start/end/height|Current start/end/height|Own height Δ|Upstream start Δ|','|---|---|---|---:|---:|']
        for name,m in sections.items():
            r=m['reference'];c=m['current'];rows.append(f"|{name}|{r['top']:.1f} / {r['bottom']:.1f} / {r['height']:.1f}|{c['top']:.1f} / {c['bottom']:.1f} / {c['height']:.1f}|{m['heightDelta']:+.1f}|{m['cumulativeStartDelta']:+.1f}|")
    (RUN/label/'metrics.md').write_text('\n'.join(rows)+'\n')
    print('\n'.join(rows))

if __name__=='__main__':
    if len(sys.argv)>1:compare(sys.argv[1])
    else:print(json.dumps(references(),ensure_ascii=False,indent=2))
