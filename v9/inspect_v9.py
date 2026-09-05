"""Independent verification of the actual saved FreeCAD document."""
from pathlib import Path
import json,math
import FreeCAD as A
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output'
doc=A.openDocument(str(OUT/'PanTilt_V9_HC-V760.FCStd'))
COLORS={'base':(.22,.28,.32),'frame':(.23,.55,.60),'cradle':(.76,.83,.84),'gear':(.94,.65,.23),'steel':(.66,.70,.74),'motor':(.12,.14,.17),'belt':(.075,.08,.09),'camera':(.14,.16,.18),'envelope':(.35,.62,.85)}
V=A.Vector;P=V(10.3,0,197)
records=[]
for o in doc.Objects:
    if not hasattr(o,'Manufacturing'):continue
    s=o.Shape.copy();parent=o.getGlobalPlacement().multiply(o.Placement.inverse());s.Placement=parent.multiply(s.Placement)
    parents=[];q=o.getParentGeoFeatureGroup()
    while q:
        parents.append(q.Name);q=q.getParentGeoFeatureGroup()
    records.append(dict(name=o.Name,shape=s,motion='Tilt' if 'Tilt' in parents else 'Pan' if 'Pan' in parents else 'Fixed',printed=o.Manufacturing=='FDM',role=o.MaterialRole))

def overlap(a,b):
    a,b=a.BoundBox,b.BoundBox
    return min(a.XMax,b.XMax)-max(a.XMin,b.XMin)>1e-5 and min(a.YMax,b.YMax)-max(a.YMin,b.YMin)>1e-5 and min(a.ZMax,b.ZMax)-max(a.ZMin,b.ZMin)>1e-5
def collisions(aa,bb,kind,angle=None):
    issues=[]
    for a in aa:
        for b in bb:
            if a['name']==b['name']:continue
            if overlap(a['shape'],b['shape']):
                vol=a['shape'].common(b['shape']).Volume
                if vol>.015:issues.append(dict(check=kind,a=a['name'],b=b['name'],volume_mm3=round(vol,5),angle=angle))
    return issues
def rotate(r,angle,axis,origin):
    t=dict(r);t['shape']=r['shape'].copy();t['shape'].rotate(origin,axis,angle);return t
printed=[r for r in records if r['printed']]
issues=[]
for i,a in enumerate(printed):issues+=collisions([a],printed[i+1:],'printed_static')
hard=[r for r in records if r['name'].startswith('H_')]
issues+=collisions(printed,hard,'fastener_vs_printed')
refs=[r for r in records if r['name'].startswith(('M0','R0','D01','D03','Camera'))]
issues+=collisions(printed,refs,'purchased_vs_printed')
print('STATIC',len(issues),flush=True)
moving=[r for r in records if r['motion']=='Tilt' and (r['printed'] or r['name'].startswith(('Camera','H_')))]
stationary=[r for r in records if r['motion']!='Tilt' and (r['printed'] or r['name'].startswith(('M02','R03','D03')))]
for angle in range(-60,61,3):
    issues+=collisions([rotate(r,angle,V(0,1,0),P) for r in moving],stationary,'tilt_sweep',angle)
print('TILT',len(issues),flush=True)
moving=[r for r in records if r['motion']!='Fixed' and (r['printed'] or r['name'].startswith(('Camera','H_','M02')))]
stationary=[r for r in records if r['motion']=='Fixed' and (r['printed'] or r['name'].startswith(('M01','R01','D01')))]
for angle in range(0,360,10):
    issues+=collisions([rotate(r,angle,V(0,0,1),V(0,0,0)) for r in moving],stationary,'pan_sweep',angle)
print('PAN',len(issues),flush=True)
angle_checks=[]
for name,axis in [('Pan',V(0,0,1)),('Tilt',V(0,1,0))]:
    o=doc.getObject(name);setattr(o,name+'Angle',30);doc.recompute();rot=o.Placement.Rotation
    correct=abs(math.degrees(rot.Angle)-30)<1e-6 and (rot.Axis-axis).Length<1e-6
    angle_checks.append(dict(part=name,axis=list(rot.Axis),angle=math.degrees(rot.Angle),correct=correct))
    setattr(o,name+'Angle',0);doc.recompute()
report={'passed':not issues and all(r['shape'].isValid() and len(r['shape'].Solids)==1 for r in printed) and all(x['correct'] for x in angle_checks),
    'printable_parts':len(printed),'issues':issues,'angle_properties':angle_checks,
    'scope':'Saved BRep solids. Pan 0..350 deg /10 deg, tilt -60..60 deg /3 deg; separate sweeps. Contact-volume threshold 0.015 mm3. Belts are nominal envelopes and excluded from tooth engagement collisions. Camera dimensions inherited, not measured. Physical fit, fatigue and load capacity not tested.'}
(OUT/'geometry_validation.json').write_text(json.dumps(report,indent=2))
meshes=[]
for r in records:
    vs,fs=r['shape'].tessellate(.12)
    meshes.append({**{k:r[k] for k in ('name','motion','role','printed')},'vertices':[list(v) for v in vs],'triangles':fs,'color':COLORS[r['role']]})
(OUT/'render_meshes.json').write_text(json.dumps(meshes,separators=(',',':')))
print('FINAL',report['passed'],'ISSUES',len(issues),flush=True)
for i in issues[:30]:print(i,flush=True)
