#!/usr/bin/env python3
"""Drop in your own head crop. Usage: python3 make-you.py <head.png> [portrait.png]
   <head.png>: transparent background, face/jaw/chin/neck/hair only — any size; it is scaled to 43×46 for the sprite.
   Rebuilds you.js (YOU_HEAD, and YOU_PORTRAIT if a second file is given). Then reload :8088."""
import sys, base64, re
from PIL import Image
def uri(im):
    import io; b=io.BytesIO(); im.save(b,'PNG'); return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
head=Image.open(sys.argv[1]).convert('RGBA'); head.thumbnail((43,46),Image.LANCZOS)
canvas=Image.new('RGBA',(43,46),(0,0,0,0)); canvas.paste(head,((43-head.width)//2,46-head.height)); canvas.save('you-head.png')
j=open('you.js').read(); j=re.sub(r'window\.YOU_HEAD="[^"]*"','window.YOU_HEAD="%s"'%uri(canvas),j)
if len(sys.argv)>2:
    p=Image.open(sys.argv[2]).convert('RGB').resize((44,52),Image.LANCZOS); p.save('you-portrait.png'); j=re.sub(r'window\.YOU_PORTRAIT="[^"]*"','window.YOU_PORTRAIT="%s"'%uri(p),j)
open('you.js','w').write(j); print('you.js rebuilt — reload the house')
