"""Native display styling and a separate fit coupon. Uses offscreen Qt."""
from pathlib import Path
import FreeCAD as A
import FreeCADGui as G
import Part,MeshPart
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output'
G.showMainWindow();doc=A.openDocument(str(OUT/'PanTilt_V9_HC-V760.FCStd'))
colors={'base':(.22,.28,.32),'frame':(.23,.55,.60),'cradle':(.76,.83,.84),'gear':(.94,.65,.23),'steel':(.66,.70,.74),'motor':(.12,.14,.17),'belt':(.075,.08,.09),'camera':(.14,.16,.18),'envelope':(.35,.62,.85)}
for o in doc.Objects:
    if hasattr(o,'MaterialRole'):
        o.ViewObject.ShapeColor=colors[o.MaterialRole];o.ViewObject.LineColor=(.12,.16,.18)
        o.ViewObject.DisplayMode='Flat Lines';o.ViewObject.LineWidth=1.
        o.ViewObject.Visibility=o.MaterialRole!='envelope';o.ViewObject.Transparency=65 if o.MaterialRole=='envelope' else 0
    elif o.TypeId=='App::Part':o.ViewObject.Visibility=True
G.activeDocument().activeView().setCameraType('Orthographic')
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll()
doc.recompute();doc.save()

# Coupon: x increases from the end with the two tiny orientation holes.
V=A.Vector;s=Part.makeBox(100,60,8)
for x,d in [(18,22.1),(50,22.3),(82,22.5)]:s=s.cut(Part.makeCylinder(d/2,10,V(x,24,-1)))
for x,d in [(10,3.3),(22,3.5),(34,3.7)]:s=s.cut(Part.makeCylinder(d/2,10,V(x,6,-1)))
for x,w in [(58,5.7),(72,5.9),(86,6.1)]:
    s=s.cut(Part.makeCylinder(1.75,10,V(x,6,-1))).cut(Part.makeBox(w,10,2.8,V(x-w/2,-.5,2.6)))
for x in (2.5,6):s=s.cut(Part.makeCylinder(.65,10,V(x,37.5,-1)))
for x,d in [(18,7.8),(50,7.9),(82,8.0)]:
    s=s.fuse(Part.makeCylinder(d/2,8,V(x,50,8))).cut(Part.makeCylinder(1.75,18,V(x,50,-1)))
assert s.isValid() and len(s.Solids)==1
MeshPart.meshFromShape(Shape=s,LinearDeflection=.05,AngularDeflection=.12,Relative=False).write(str(OUT/'stl'/'CAL_Fit_coupon.stl'))
s.exportStep(str(OUT/'step'/'CAL_Fit_coupon.step'))
print('STYLED_AND_COUPON_SAVED',flush=True)
