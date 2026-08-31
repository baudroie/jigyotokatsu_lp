"""Aggregate only this run's diagnostic outputs; never edit implementation/assets."""
from pathlib import Path
from PIL import Image, ImageDraw
from html.parser import HTMLParser
import json, hashlib, difflib
from compare import compare, references

RUN=Path(__file__).resolve().parent;ROOT=RUN.parents[1]
def read(p):return json.loads(p.read_text())
def save(name,obj):(RUN/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

for label in ('before','loop1','loop2','final','after','after-final'):compare(label)
ref=references()
before=read(RUN/'before/layout-metrics.json');after=read(RUN/'after-final/layout-metrics.json')
combined={kind:{name:{'reference':a['reference'],'before':before[kind][name]['current'],'after':a['current'],'beforeHeightDelta':before[kind][name]['heightDelta'],'afterHeightDelta':a['heightDelta'],'beforeCumulativeStartDelta':before[kind][name]['cumulativeStartDelta'],'afterCumulativeStartDelta':a['cumulativeStartDelta'],'afterEndDelta':a['endDelta']} for name,a in sections.items()} for kind,sections in after.items()}
save('layout-metrics.json',combined)

files={int(p.stem):p for folder in ('responsive-final','responsive-after','after','after-final') for p in (RUN/folder).glob('*.json') if p.stem.isdigit()}
audit={};results=[]
for width,path in sorted(files.items()):
    data=read(path);images=data['images'];cards=[i for i in images if '/new-20260831/' in i['currentSrc']]
    expectedVariant='sp' if width<=767 else 'pc'
    correct=all(('_sp.' in i['currentSrc'] or '/sp_' in i['currentSrc'])==(expectedVariant=='sp') for i in cards)
    seq=[Path(i['currentSrc']).name for i in cards]
    expected=[f'benefit_{n:02}_{expectedVariant}.png' for n in range(1,4)]+[f'{expectedVariant}_{stem}.png' for stem in ('01_year1_candidate','02_year2-3_advisor','03_year4-5_business-head','04_year6-plus_president')]
    assert seq==expected,(width,seq)
    clipped=[i['src'] for i in images if i['visible'] and i['clipping']]
    distorted=[i['src'] for i in images if i['visible'] and abs(i['height']-i['width']*i['naturalHeight']/i['naturalWidth'])>.1]
    errors=[i['src'] for i in images if i['visible'] and (not i['complete'] or not i['naturalWidth'])]
    assert not clipped and not distorted and not errors
    assert data['viewport']['scrollWidth']==data['viewport']['clientWidth']==width
    for i in images:
        p=ROOT/i['currentSrc'].split(':4173/')[-1]
        if p.is_file():
            im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox();i['alphaBounds']=box
            i['alphaBounds128']=im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            if box and i['visible']:
                s=i['width']/im.width;i['visibleContent']={'left':i['left']+box[0]*s,'top':i['top']+box[1]*s,'width':(box[2]-box[0])*s,'height':(box[3]-box[1])*s}
    audit[str(width)]=images
    results.append({'width':width,'screenshot':str(path.with_suffix('.png').relative_to(RUN)),'pageHeight':data['viewport']['pageHeight'],'visibleImageCount':sum(i['visible'] for i in images),'cardCount':len(cards),'variant':expectedVariant,'orderAndCurrentSrc':'PASS' if correct and seq==expected else 'NG','clippedImages':clipped,'distortedImages':distorted,'loadErrors':errors,'horizontalOverflow':data['viewport']['scrollWidth']-width,'fonts':data['fonts']})
save('image-layout-audit.json',audit);save('responsive-results.json',results)

class Markup(HTMLParser):
    def __init__(self):super().__init__();self.resources=[];self.pictures=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='picture':self.pictures+=1
        if tag in ('img','source','script'):self.resources.append(a.get('src',a.get('srcset','')))
        if tag=='link' and a.get('rel')=='stylesheet':self.resources.append(a['href'].split('?')[0])
p=Markup();p.feed((ROOT/'index.html').read_text());assert p.pictures==7
missing=[x for x in p.resources if x and not (ROOT/x).is_file()];assert not missing,missing
mapping=read(RUN/'asset-map.json')
for e in mapping:assert sha(ROOT/e['destination'])==e['sha256']
original=read(RUN/'original-checksums.json');changed=[name for name,digest in original.items() if sha(ROOT/name)!=digest];assert not changed,changed
save('static-validation.json',{'pictureCount':p.pictures,'mappedAssets':len(mapping),'allPlacedAssetsByteIdentical':True,'originalFilesChecked':len(original),'changedOriginalFiles':changed,'missingResources':missing,'scriptJsUnchanged':sha(ROOT/'script.js')==sha(RUN/'code-before/script.js'),'git':'not a git repository','build':'static HTML/CSS/JS; no package.json/build step','javascriptSyntax':'node --check script.js: PASS'})
diff=''
for filename in ('index.html','styles.css','asset-map.json','README.md'):
    diff+=''.join(difflib.unified_diff((RUN/'code-before'/filename).read_text().splitlines(True),(ROOT/filename).read_text().splitlines(True),fromfile='before/'+filename,tofile='after/'+filename))
(RUN/'changes.patch').write_text(diff)

# Compact visual index of actual full-page captures, preserving their ratios.
thumbs=[]
for row in results:
    im=Image.open(RUN/row['screenshot']).convert('RGB');im.thumbnail((160,1200))
    cell=Image.new('RGB',(180,1250),'#dedede');cell.paste(im,((180-im.width)//2,36));ImageDraw.Draw(cell).text((10,10),str(row['width'])+'px',fill='black');thumbs.append(cell)
sheet=Image.new('RGB',(180*len(thumbs),1250),'#dedede')
for n,im in enumerate(thumbs):sheet.paste(im,(n*180,0))
sheet.save(RUN/'responsive-contact-sheet.jpg')
pc=Image.open(RUN/'after-final/1440.png').convert('RGB');sp=Image.open(RUN/'after-final/390.png').convert('RGB')
pc=pc.resize((440,round(pc.height*440/pc.width)));sp=sp.resize((160,round(sp.height*160/sp.width)))
preview=Image.new('RGB',(620,max(pc.height,sp.height)+30),'#eee');preview.paste(pc,(0,30));preview.paste(sp,(460,30));d=ImageDraw.Draw(preview);d.text((10,8),'Desktop 1440px',fill='black');d.text((462,8),'Mobile 390px',fill='black');preview.save(RUN/'after-final/preview.jpg')
# Screenshot excerpts only: every selected card is included in full.
card_preview=Image.new('RGB',(1000,370),'#eee');draw=ImageDraw.Draw(card_preview)
draw.text((10,8),'Desktop: all 7 cards',fill='black');draw.text((620,8),'Mobile: card 01 examples (full page linked)',fill='black')
pc=Image.open(RUN/'after-final/1440.png').convert('RGB');sp=Image.open(RUN/'after-final/390.png').convert('RGB')
y=30
for section in ('benefits','career'):
    m=after['desktop'][section]['current'];im=pc.crop((0,round(m['top']),1440,round(m['bottom'])));im=im.resize((600,round(im.height*600/1440)));card_preview.paste(im,(0,y));y+=im.height+8
for x,section in [(620,'benefits'),(810,'career')]:
    entry=next(i for i in audit['390'] if '/new-20260831/' in i['currentSrc'] and ('benefit_01' if section=='benefits' else 'sp_01') in i['currentSrc'])
    im=sp.crop((round(entry['left']),round(entry['top']),round(entry['right']),round(entry['bottom'])));im=im.resize((180,round(im.height*180/im.width)));card_preview.paste(im,(x,32))
card_preview.save(RUN/'after-final/cards-preview.jpg')
print(json.dumps(results,ensure_ascii=False,indent=2))
