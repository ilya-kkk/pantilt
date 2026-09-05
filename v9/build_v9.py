"""Reproducible FreeCAD V9. Units mm; X forward, Y left, Z up.
Imports only geometry helpers from the preserved V8 generator.
"""
from pathlib import Path
import sys, math, json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import FreeCAD as A
import Part, MeshPart
import build_pantilt_freecad as old
from build_pantilt_freecad import vec,box,cyl_z,cyl_y,cyl_x,ring_z,ring_y,prism_z,prism_y,slot_z,slot_y
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
C=json.loads((ROOT/'fit_parameters.json').read_text())
TX,TZ=10.3,197.;TOP=TZ-36.5;PIVOT=vec(TX,0,TZ)
COLORS={'base':(.22,.28,.32),'frame':(.23,.55,.60),'cradle':(.76,.83,.84),'gear':(.94,.65,.23),'steel':(.66,.70,.74),'motor':(.12,.14,.17),'belt':(.075,.08,.09),'camera':(.14,.16,.18),'envelope':(.35,.62,.85)}
records=[];hardware=[];fillets=[]
def union(*ss):
    s=ss[0]
    for o in ss[1:]:s=s.fuse(o)
    return s.removeSplitter()
def move(s,p):
    s=s.copy();s.translate(vec(*p));return s
def turn(s,a,axis=(0,0,1),origin=(0,0,0)):
    s=s.copy();s.rotate(vec(*origin),vec(*axis),a);return s
def pose(s,p,axis=(0,0,1),feed=None):
    z=vec(*axis)
    rot=A.Rotation(vec(0,0,1),z) if feed is None else A.Rotation(vec(*feed),z.cross(vec(*feed)),z,'ZXY')
    s=s.copy();s.Placement=A.Placement(vec(*p),rot).multiply(s.Placement);return s
def hole(p,axis,length,d=None):return Part.makeCylinder((d or C['m3_hole_d'])/2,length,vec(*p),vec(*axis))
def nut_trap(p,axis=(0,0,1),feed=(1,0,0),reach=12):
    return pose(box(reach+3.5,C['nut_slot_width'],C['nut_slot_thickness'],((reach-3.5)/2,0,0)),p,axis,feed)
def cbore(seat,axis):
    p=vec(*seat)-vec(*axis)*(C['head_recess_depth']+.1)
    return hole(tuple(p),axis,C['head_recess_depth']+.11,C['head_recess_d'])
def rounded(s,axis,r,label='profile'):
    av=vec(*axis);edges=[]
    for e in s.Edges:
        if len(e.Vertexes)!=2:continue
        v=e.Vertexes[1].Point-e.Vertexes[0].Point
        if v.Length>1e-5 and v.cross(av).Length<1e-6 and abs(e.Length-v.Length)<1e-5:edges.append(e)
    if edges:
        for radius in sorted(set([r,min(r,2),min(r,1)]),reverse=True):
            try:
                t=s.makeFillet(radius,edges)
                if t.isValid() and len(t.Solids)==1:
                    fillets.append({'part':label,'radius':radius});return t
            except Exception:pass
    fillets.append({'part':label,'radius':0});return s
def rbox(l,w,h,p,r=3):return rounded(box(l,w,h,p),(0,0,1),r)
def add(name,s,motion='Fixed',role='base',printed=True,print_axis=(0,0,1),note=''):
    s=s.removeSplitter();o=doc.addObject('PartDesign::Feature',name);o.Label=name.replace('_',' ');groups[motion].addObject(o)
    o.Shape=move(s,tuple(-PIVOT)) if motion=='Tilt' else s
    for prop,value in [('PartNumber',name),('MaterialRole',role),('Manufacturing','FDM' if printed else 'Reference / purchased'),('AssemblyNote',note)]:
        o.addProperty('App::PropertyString',prop,'V9');setattr(o,prop,value)
    o.addProperty('App::PropertyVector','PrintBedNormal','V9');o.PrintBedNormal=vec(*print_axis)
    records.append({'name':name,'shape':s,'motion':motion,'role':role,'printed':printed,'print_axis':print_axis,'object':o});return o
def hex_prism(af,h,z):
    r=af/math.sqrt(3);return prism_z([(r*math.cos(i*math.pi/3),r*math.sin(i*math.pi/3)) for i in range(6)],h,z)
def screw(name,seat,axis,length,motion='Fixed',nut=None,feed=(1,0,0)):
    sh=union(cyl_z(1.5,length,(0,0,length/2)),cyl_z(2.75,3,(0,0,-1.5))).cut(hex_prism(2.5,1.6,-3.1))
    add('H_'+name,pose(sh,seat,axis),motion,'steel',False)
    if nut is not None:
        nh=hex_prism(5.5,2.4,-1.2).cut(cyl_z(1.25,4,(0,0,0)))
        add('H_'+name+'_nut',pose(nh,nut,axis,feed),motion,'steel',False)
    hardware.append({'name':name,'thread':'M3','standard':'DIN 912','length_mm':length,'nut':nut is not None,'seat':seat,'axis':axis})
def centre_distance(length,R,r):
    lo,hi=R-r+.01,length
    for _ in range(80):
        c=(lo+hi)/2;d=R-r;L=2*math.sqrt(c*c-d*d)+math.pi*(R+r)+2*math.asin(d/c)*d
        if L>length:hi=c
        else:lo=c
    return (lo+hi)/2
MX=-centre_distance(350,120/math.pi,20/math.pi);TMX=TX-46
TMZ=TZ-math.sqrt(centre_distance(280,80/math.pi,20/math.pi)**2-46**2)
doc=A.newDocument('PanTilt_V9');assembly=doc.addObject('App::Part','Assembly');assembly.Label='PanTilt V9 — HC-V760';groups={}
for name in ('Fixed','Pan','Tilt'):
    groups[name]=doc.addObject('App::Part',name);(groups['Pan'] if name=='Tilt' else assembly).addObject(groups[name])
groups['Tilt'].Placement.Base=PIVOT
for name,axis in [('Pan',(0,0,1)),('Tilt',(0,1,0))]:
    g=groups[name];prop=name+'Angle';g.addProperty('App::PropertyAngle',prop,'Motion');setattr(g,prop,0)
    g.Placement.Rotation=A.Rotation(vec(*axis),0);g.setExpression('Placement.Rotation.Angle',prop)

# Pedestal and removable lap-jointed feet.
base=union(cyl_z(58,10,(0,0,5)),cyl_z(28,66,(0,0,43)))
try:base=base.makeFillet(6,[e for e in base.Edges if abs(e.CenterOfMass.z-10)<.01 and abs(e.Length-2*math.pi*28)<.1])
except Exception:pass
for cut in [cyl_z(7.5,80,(0,0,36)),cyl_z(9,.6,(0,0,63.7)),cyl_z(C['bearing_608_pocket_d']/2,12.5,(0,0,70.25)),cyl_z(24.2,6,(0,0,72.5)),cyl_z(C['thrust_seat_d']/2,2,(0,0,76))]:base=base.cut(cut)
for angle in (0,120,240):
    base=base.cut(turn(box(29,28.4,5.2,(48.5,0,2.6)),angle))
    for x in (42,53):base=base.cut(turn(hole((x,0,-1),(0,0,1),12),angle))
base=base.cut(box(31,38.4,5.2,(-48.5,0,2.6)))
for y in (-12,12):base=base.cut(hole((-45,y,-1),(0,0,1),12))
cap=ring_z(48,15,5,(0,0,72)).cut(cyl_z(11.25,1.8,(0,0,70.3)))
for i,angle in enumerate((30,150,270)):
    a=math.radians(angle);x,y=19*math.cos(a),19*math.sin(a);feed=(math.cos(a),math.sin(a),0)
    base=base.cut(hole((x,y,58),(0,0,1),20)).cut(nut_trap((x,y,65),feed=feed))
    cap=cap.cut(hole((x,y,68),(0,0,1),8)).cut(cbore((x,y,71.2),(0,0,-1)))
    screw('Pan608_cap_'+str(i),(x,y,71.2),(0,0,-1),10,nut=(x,y,65),feed=feed)
add('B01_Central_pedestal',base)
for i,angle in enumerate((0,120,240)):
    s=rounded(prism_z([(35,-11),(110,-17),(140,-10),(140,10),(110,17),(35,11)],8,0),(0,0,1),4,'Leg')
    s=s.cut(box(28,40,4,(47,0,7))).cut(slot_z(38,9,10,(94,0,4))).cut(hole((128,0,-1),(0,0,1),10))
    for j,x in enumerate((42,53)):
        s=s.cut(hole((x,0,-1),(0,0,1),10)).cut(nut_trap((x,0,2.5),feed=(0,1,0),reach=14))
        a=math.radians(angle);xx,yy=x*math.cos(a),x*math.sin(a)
        screw('Leg_%s_%s'%(i,j),(xx,yy,10),(0,0,-1),10,nut=(xx,yy,2.5),feed=(-math.sin(a),math.cos(a),0))
    add('B02_Leg_'+str(i+1),turn(s,angle))
foot=union(rbox(76,72,8,(MX-1,0,4),5),box(32.6,38,5,(-49.5,0,2.5)))
for y in (-12,12):
    feed=(0,1 if y>0 else -1,0)
    foot=foot.cut(hole((-45,y,-1),(0,0,1),10)).cut(nut_trap((-45,y,2.5),feed=feed))
    screw('Motor_foot_'+str(y),(-45,y,10),(0,0,-1),10,nut=(-45,y,2.5),feed=feed)
deck=rbox(76,72,6,(MX,0,61),5)
for side in (-1,1):
    y=side*30;wall=rounded(box(70,8,50,(MX,y,33)),(0,1,0),3,'Motor stand')
    wall=wall.cut(rounded(box(34,12,23,(MX,y,33)),(0,1,0),5))
    for j,x in enumerate((MX-28,MX+28)):
        foot=foot.cut(hole((x,y,-1),(0,0,1),11)).cut(cbore((x,y,3.3),(0,0,1)))
        wall=wall.cut(hole((x,y,7),(0,0,1),15)).cut(nut_trap((x,y,15),feed=(0,side,0),reach=7))
        screw('Stand_bottom_%s_%s'%(side,j),(x,y,3.3),(0,0,1),16,nut=(x,y,15),feed=(0,side,0))
        wall=wall.cut(hole((x,y,46),(0,0,1),14)).cut(nut_trap((x,y,52),feed=(0,side,0),reach=7))
        deck=deck.cut(hole((x,y,57),(0,0,1),9)).cut(cbore((x,y,60.7),(0,0,-1)))
        screw('Stand_top_%s_%s'%(side,j),(x,y,60.7),(0,0,-1),12,nut=(x,y,52),feed=(0,side,0))
    add('B04_Motor_stand_'+str(side),wall,print_axis=(0,side,0))
deck=deck.cut(slot_z(36.6,22.6,10,(MX,0,61)))
for i,dx in enumerate((-15.5,15.5)):
    for j,y in enumerate((-15.5,15.5)):
        x=MX+dx;deck=deck.cut(slot_z(14+C['m3_hole_d'],C['m3_hole_d'],10,(x,y,61)))
        deck=deck.cut(slot_z(14+C['head_recess_d'],C['head_recess_d'],3.4,(x,y,62.4)))
        screw('Pan_motor_%s_%s'%(i,j),(x,y,60.7),(0,0,-1),6)
add('B03_Motor_stand_foot',foot);add('B05_Pan_motor_deck',deck);add('B06_Pan_608_retainer',cap,print_axis=(0,0,-1))
motor=union(box(42,42,48,(MX,0,34)),cyl_z(11,2,(MX,0,59)),cyl_z(2.5,24,(MX,0,70)))
add('M01_Pan_NEMA17',motor,role='motor',printed=False)
add('R01_Pan_608',ring_z(22,8,7,(0,0,67.5)),role='steel',printed=False)
add('R02_51107_lower',ring_z(52,37,3.5,(0,0,76.75)),role='steel',printed=False)
balls=Part.makeCompound([Part.makeSphere(3,vec(21.5*math.cos(i*2*math.pi/11),21.5*math.sin(i*2*math.pi/11),81)) for i in range(11)])
add('R02_51107_rolling_envelope',balls,role='steel',printed=False)
add('R02_51107_upper',ring_z(52,35,3.5,(0,0,85.25)),'Pan','steel',False)

# Rotor and platform; print rotor upside down.
gear,pan_metrics=old.gt2_2mr_pulley_z(120,11,(0,0,75),bore=58,flanges=False)
rotor=union(gear,ring_z(76,58,6,(0,0,83)),cyl_z(38,6,(0,0,89)),cyl_z(17.3,11.7,(0,0,81.15)),cyl_z(C['journal_d']/2,22.2,(0,0,74.9)),cyl_z(5.75,4.1,(0,0,73.25)))
rotor=rotor.cut(ring_z(52.4,34.8,1.1,(0,0,86.45))).cut(hole((0,0,60),(0,0,1),35)).cut(nut_trap((0,0,79),reach=20))
platform=rbox(166,176,8,(-8,0,96),10)
for i,angle in enumerate((45,135,225,315)):
    a=math.radians(angle);x,y=32*math.cos(a),32*math.sin(a);feed=(math.cos(a),math.sin(a),0)
    rotor=rotor.cut(hole((x,y,82),(0,0,1),12)).cut(nut_trap((x,y,88.5),feed=feed,reach=9))
    platform=platform.cut(hole((x,y,91),(0,0,1),10)).cut(cbore((x,y,96.7),(0,0,-1)))
    screw('Rotor_platform_'+str(i),(x,y,96.7),(0,0,-1),10,'Pan',nut=(x,y,88.5),feed=feed)
add('P01_Pan_rotor_120T',rotor,'Pan','gear',print_axis=(0,0,-1))
add('P02_Pan_axial_retainer',ring_z(11.5,C['m3_hole_d'],2,(0,0,62.8)),'Pan','cradle')
screw('Pan_axial',(0,0,61.8),(0,0,1),20,'Pan',nut=(0,0,79))
for side,yc in ((1,71),(-1,-61.5)):
    if side==1:
        f=box(128,18,14,(-12,yc,107));arm=prism_y([(-57,111),(-28,111),(5,183),(-4,193),(-20,175),(-57,129)],14,66)
        boss=cyl_y(20,17,(TX,71.5,TZ));front=80
    else:
        f=box(128,17,14,(-12,yc+.5,107));arm=prism_y([(-76,105),(52,105),(52,114),(31,114),(28,219),(-28,219),(-31,157),(-76,157)],13,yc-8)
        boss=cyl_y(20,16,(TX,yc,TZ));front=-69.5
    s=rounded(union(f,arm,boss),(0,1,0),3,'Yoke '+str(side))
    s=s.cut(hole((TX,front+side*.1,TZ),(0,-side,0),7.4,C['bearing_608_pocket_d'])).cut(hole((TX,yc-15,TZ),(0,1,0),30,15))
    s=s.fuse(box(88,8,2,(-12,yc,99)));platform=platform.cut(box(88.4,8.4,2.2,(-12,yc,99)))
    for j,x in enumerate((-52,0,34)):
        s=s.cut(hole((x,yc,97),(0,0,1),17)).cut(nut_trap((x,yc,108),feed=(0,side,0)))
        platform=platform.cut(hole((x,yc,91),(0,0,1),11)).cut(cbore((x,yc,95.3),(0,0,1)))
        screw('Yoke_base_%s_%s'%(side,j),(x,yc,95.3),(0,0,1),16,'Pan',nut=(x,yc,108),feed=(0,side,0))
    if side==-1:
        s=s.cut(slot_y(36.6,22.6,20,(TMX,yc,TMZ),along='x'))
        for i,dx in enumerate((-15.5,15.5)):
            for j,dz in enumerate((-15.5,15.5)):
                x,z=TMX+dx,TMZ+dz
                s=s.cut(slot_y(14+C['m3_hole_d'],C['m3_hole_d'],20,(x,yc,z),along='x')).cut(slot_y(14+C['head_recess_d'],C['head_recess_d'],4.4,(x,yc+2.8,z),along='x'))
                screw('Tilt_motor_%s_%s'%(i,j),(x,yc+.7,z),(0,-1,0),12,'Pan')
        m=union(box(42,48,42,(TMX,front-24,TMZ)),cyl_y(11,2,(TMX,front+1,TMZ)),cyl_y(2.5,24,(TMX,front+12,TMZ)))
        add('M02_Tilt_NEMA17',m,'Pan','motor',False)
    cap=union(ring_y(44,15,4,(TX,front+side*2,TZ)),ring_y(21.8,18.5,.2,(TX,front-side*.1,TZ)))
    for i,angle in enumerate((90,210,330)):
        a=math.radians(angle);dx,dz=16.5*math.cos(a),16.5*math.sin(a);x,z=TX+dx,TZ+dz
        feed=(math.cos(a),0,math.sin(a));n=(x,yc+side,z);seat=(x,front+side*.7,z)
        s=s.cut(hole((x,yc-12,z),(0,1,0),25)).cut(nut_trap(n,(0,side,0),feed,8))
        cap=cap.cut(hole((x,front-6,z),(0,1,0),12)).cut(cbore(seat,(0,-side,0)))
        screw('Tilt608_cap_%s_%s'%(side,i),seat,(0,-side,0),10,'Pan',nut=n,feed=feed)
    add('P04_Yoke_'+('left' if side==1 else 'right'),s,'Pan','frame',print_axis=(0,-side,0))
    add('P05_608_cap_'+str(side),cap,'Pan','cradle',print_axis=(0,-side,0))
    add('R03_Tilt608_'+str(side),ring_y(22,8,7,(TX,front-side*3.7,TZ)),'Pan','steel',False)
add('P03_Pan_platform',platform,'Pan','frame')

# Short camera saddle, independent trunnions; no through axle.
saddle=rbox(39,108,8,(10,10,TOP-4),3).cut(slot_z(28,7,10,(10,0,TOP-4)))
for side,yc,fy,cl in ((1,57,59,32),(-1,-37,-39,60)):
    cheek=rounded(union(box(cl,6,39,(TX,yc,TOP+19.5)),cyl_y(13,6,(TX,yc,TZ))),(0,1,0),3,'Cheek '+str(side))
    cheek=union(cheek,rbox(32,10,12,(TX,fy,TOP+6),3),box(28,6,2,(TX,fy,TOP-1)))
    saddle=saddle.cut(box(28.4,6.4,2.2,(TX,fy,TOP-1)))
    for j,x in enumerate((TX-10,TX+10)):
        cheek=cheek.cut(hole((x,fy,TOP-3),(0,0,1),17)).cut(nut_trap((x,fy,TOP+8),feed=(0,side,0),reach=8))
        saddle=saddle.cut(hole((x,fy,TOP-9),(0,0,1),11)).cut(cbore((x,fy,TOP-8+3.3),(0,0,1)))
        screw('Cradle_foot_%s_%s'%(side,j),(x,fy,TOP-8+3.3),(0,0,1),16,'Tilt',nut=(x,fy,TOP+8),feed=(0,side,0))
    if side==1:
        cheek=union(cheek,cyl_y(9,2.6,(TX,61.3,TZ)),cyl_y(5.75,10,(TX,67.6,TZ)),cyl_y(C['journal_d']/2,7.4,(TX,76.3,TZ)))
        nut=(TX,58.5,TZ);seat=(TX,82,TZ);length=25;rcy=81
    else:
        gear,tilt_metrics=old.gt2_2mr_pulley_y(80,11,(TX,-45.8,TZ),flanges=False)
        cheek=union(cheek,gear,cyl_y(tilt_metrics['compensated_outside_diameter_mm']/2,6.3,(TX,-37.15,TZ)),cyl_y(5.75,10.8,(TX,-56.7,TZ)),cyl_y(C['journal_d']/2,7.4,(TX,-65.8,TZ)))
        nut=(TX,-38.2,TZ);seat=(TX,-71.5,TZ);length=35;rcy=-70.5
    cheek=cheek.cut(hole((TX,yc-40,TZ),(0,1,0),80)).cut(nut_trap(nut,(0,side,0),(1,0,0),cl/2+2))
    add('T02_Cheek_'+('left' if side==1 else 'right_80T'),cheek,'Tilt','cradle' if side==1 else 'gear',print_axis=(0,-side,0))
    add('T03_Axial_retainer_'+str(side),ring_y(11.5,C['m3_hole_d'],2,(TX,rcy,TZ)),'Tilt','cradle',print_axis=(0,1,0))
    screw('Tilt_axial_'+str(side),seat,(0,-side,0),length,'Tilt',nut=nut)
add('T01_Camera_saddle',saddle,'Tilt','cradle')
def metal_pulley():return union(ring_z(12.3,5,11,(0,0,0)),ring_z(18,5,1,(0,0,-6)),ring_z(18,5,1,(0,0,6)),ring_z(16,5,5,(0,0,-9)))
add('D01_Pan_20T',pose(metal_pulley(),(MX,0,75)),'Fixed','steel',False)
add('D02_Pan_belt_350',old.belt_z((0,0),240/math.pi,(MX,0),40/math.pi,75),'Fixed','belt',False)
add('D03_Tilt_20T',pose(metal_pulley(),(TMX,-45.8,TMZ),(0,1,0)),'Pan','steel',False)
add('D04_Tilt_belt_280',old.belt_y((TX,TZ),160/math.pi,(TMX,TMZ),40/math.pi,-45.8),'Pan','belt',False)
camera=union(rbox(139,65,73,(0,0,TZ),5),cyl_x(18,20,(79.5,0,TZ+2)),rbox(18,48,52,(-76.5,0,TZ),3))
add('Camera_HC_V760_envelope',camera,'Tilt','camera',False)
add('Camera_LCD_open_envelope',box(4,68,45,(35,66.5,TZ)),'Tilt','envelope',False)
add('Camera_HDMI_envelope',box(24,20,16,(TX,42.5,TZ-10)),'Tilt','envelope',False)
sheet=doc.addObject('Spreadsheet::Sheet','Parameters');sheet.Label='Dimensions — edit JSON and regenerate'
data={'Tilt axis X':TX,'Tilt axis Z':TZ,'Pan motor X':MX,'Tilt motor X':TMX,'Tilt motor Z':TMZ,**C}
for row,(k,v) in enumerate(data.items(),1):sheet.set('A'+str(row),k);sheet.set('B'+str(row),str(v))
sheet.setColumnWidth('A',235);doc.recompute()
checks=[]
for r in records:
    s=r['shape']
    if r['printed']:
        checks.append({'name':r['name'],'valid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume})
        if not s.isValid() or len(s.Solids)!=1:raise RuntimeError('Invalid printable part: '+r['name'])
doc.saveAs(str(OUT/'PanTilt_V9_HC-V760.FCStd'))
(OUT/'stl').mkdir(exist_ok=True);(OUT/'step').mkdir(exist_ok=True)
for r in records:
    if not r['printed']:continue
    s=r['shape'].copy();s.Placement=A.Placement(vec(0,0,0),A.Rotation(vec(*r['print_axis']),vec(0,0,1))).multiply(s.Placement)
    b=s.BoundBox;s.translate(vec(-b.XMin,-b.YMin,-b.ZMin))
    MeshPart.meshFromShape(Shape=s,LinearDeflection=.06,AngularDeflection=.12,Relative=False).write(str(OUT/'stl'/(r['name']+'.stl')))
    r['shape'].exportStep(str(OUT/'step'/(r['name']+'.step')))
# Export world-space clones: Part.export on nested individual features does not
# apply their enclosing App::Part placements consistently.
ex=A.newDocument('V9_STEP_export');export_objects=[]
for r in records:
    o=ex.addObject('PartDesign::Feature',r['name']);o.Label=r['object'].Label;o.Shape=r['shape'];export_objects.append(o)
Part.export(export_objects,str(OUT/'PanTilt_V9_assembly.step'))
A.closeDocument(ex.Name);A.setActiveDocument(doc.Name)
(OUT/'hardware.json').write_text(json.dumps(hardware,indent=2))
(OUT/'build_report.json').write_text(json.dumps({'parts':checks,'fillets':fillets,'pan_gt2':pan_metrics,'tilt_gt2':tilt_metrics,'parameters':data},indent=2))
print('BUILD_COMPLETE',len(checks),'printable parts',flush=True)
