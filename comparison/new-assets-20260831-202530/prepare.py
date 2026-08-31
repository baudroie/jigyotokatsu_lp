"""Only copies original bytes; images produced here are separate QA previews."""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from PIL import Image, ImageDraw
import json, hashlib, shutil

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
EXPECTED = [f'benefit_{n:02}_{v}.png' for v in ('pc','sp') for n in range(1,4)]
EXPECTED += [f'{v}_{stem}.png' for v in ('pc','sp') for stem in ('01_year1_candidate','02_year2-3_advisor','03_year4-5_business-head','04_year6-plus_president')]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,data): (RUN/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    backup=RUN/'code-before';backup.mkdir(exist_ok=True)
    for file in ('index.html','styles.css','script.js','README.md','asset-map.json'):
        dest=backup/file
        if not dest.exists(): shutil.copy2(ROOT/file,dest)
    originals={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*.png') if 'comparison' not in p.parts}
    originals['新素材.zip']=sha(ROOT/'新素材.zip')
    dump('original-checksums.json',originals)
    entries=[]
    with ZipFile(ROOT/'新素材.zip') as z:
        for filename in EXPECTED:
            found=[i for i in z.infolist() if PurePosixPath(i.filename).name==filename and not any(p=='__MACOSX' or p=='.DS_Store' or p.startswith('._') for p in PurePosixPath(i.filename).parts)]
            assert len(found)==1,(filename,len(found))
            info=found[0]
            assert not PurePosixPath(info.filename).is_absolute() and '..' not in PurePosixPath(info.filename).parts
            extracted=RUN/'extracted'/filename
            extracted.parent.mkdir(exist_ok=True)
            with extracted.open('xb') as f: f.write(z.read(info))
            im=Image.open(extracted).convert('RGBA')
            alpha=im.getchannel('A')
            section='benefits' if filename.startswith('benefit') else 'career'
            variant='sp' if '_sp.' in filename or filename.startswith('sp_') else 'pc'
            expected=(1040,1600) if variant=='sp' else ((1600,960) if section=='benefits' else (1600,1040))
            assert im.size==expected,(filename,im.size)
            dest=Path('assets')/('cards' if section=='benefits' else 'career')/'new-20260831'/filename
            entries.append(dict(zipMember=info.filename,extracted=str(extracted.relative_to(ROOT)),destination=str(dest),section=section,variant=variant,width=im.width,height=im.height,aspectRatio=im.width/im.height,alphaExtrema=alpha.getextrema(),alphaBounds=alpha.getbbox(),alphaBounds128=alpha.point(lambda a:255 if a>=128 else 0).getbbox(),sha256=sha(extracted)))
    dump('asset-map.json',entries)
    for variant in ('pc','sp'):
        subset=[e for e in entries if e['variant']==variant]
        board=Image.new('RGB',(4*360,2*600),'#e9e9e9');draw=ImageDraw.Draw(board)
        for i,e in enumerate(subset):
            x=(i%4)*360;y=(i//4)*600
            im=Image.open(ROOT/e['extracted']).convert('RGBA');im.thumbnail((350,550))
            board.paste(im,(x+(360-im.width)//2,y+35),im)
            draw.text((x+5,y+8),Path(e['destination']).name,fill='black')
        board.save(RUN/f'assets-{variant}.jpg')
    refs={}
    for variant,term in [('desktop','*案web.png'),('mobile','*案mobile.png')]:
        path=next(ROOT.glob(term));im=Image.open(path)
        refs[variant]={'file':path.name,'width':im.width,'height':im.height,'sha256':sha(path)}
    dump('reference-files.json',refs)
    print(json.dumps(entries,ensure_ascii=False,indent=2))
