"""Render tessellations produced by inspect_v9.py, using a CPU depth buffer."""
from pathlib import Path
import json,struct,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output';VIEW=OUT/'views';VIEW.mkdir(exist_ok=True)
data=json.loads((OUT/'render_meshes.json').read_text())
subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'render_cpu.cpp'),'-o',str(ROOT/'render_cpu')],check=True)
def render(name,az=315,el=24,tilt=0,camera=True,exploded=False):
    chunks=[]
    for r in data:
        if r['role']=='envelope' or (not camera and r['role']=='camera'):continue
        v=np.array(r['vertices']);t=np.array(r['triangles'])
        if tilt and r['motion']=='Tilt':
            a=math.radians(tilt);m=np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
            p=np.array([10.3,0,197]);v=(v-p)@m.T+p
        if exploded:
            if r['name'].startswith('H_'):continue
            if r['role']=='belt':continue
            n=r['name'];side=1 if np.mean(v[:,1])>0 else -1
            if n=='R02_51107_upper':v[:,2]+=20
            elif n.startswith('P01'):v[:,2]+=50
            elif n.startswith('P02'):v[:,2]+=40
            elif n.startswith('P03'):v[:,2]+=105
            elif n.startswith(('P04','P05','R03','M02','D03')):
                v[:,2]+=140;v[:,1]+=side*(50 if n.startswith('P05') else 42 if n.startswith('R03') else 35)
            elif r['motion']=='Tilt':
                v[:,2]+=170
                if n.startswith(('T02','T03')):v[:,1]+=side*(50 if n.startswith('T03') else 35)
        faces=v[t].reshape(-1,9);col=np.tile(r['color'],(len(t),1));chunks.append(np.hstack([faces,col]).astype('<f4'))
    triangles=np.concatenate(chunks);binary=VIEW/(name+'.bin');ppm=VIEW/(name+'.ppm')
    binary.write_bytes(struct.pack('<I',len(triangles))+triangles.tobytes())
    subprocess.run([str(ROOT/'render_cpu'),str(binary),str(ppm),str(az),str(el),'2400','1800'],check=True)
    im=Image.open(ppm).resize((1600,1200),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    d.text((55,30),'PAN / TILT V9',font=ImageFont.truetype(font,32),fill='#22323a')
    detail='HC-V760  /  NEMA17  /  GT2-10  /  M3'
    if tilt:detail+='  /  Tilt '+str(tilt)+'°'
    if exploded:detail='Exploded component overview (fasteners hidden)'
    d.text((56,76),detail,font=ImageFont.truetype(font,18),fill='#54626a')
    im.save(VIEW/(name+'.png'));binary.unlink();ppm.unlink()
for args in [('01_assembly',315,24,0,True,False),('02_mechanism',315,28,0,False,False),('03_left_rear',135,24,0,False,False),('04_tilt_plus60',315,20,60,True,False),('05_tilt_minus60',315,20,-60,True,False),('06_exploded',315,23,0,False,True)]:
    render(*args);print(args[0],flush=True)
