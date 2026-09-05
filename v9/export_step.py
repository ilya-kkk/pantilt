"""Export global geometry from a saved native assembly, preserving part names."""
from pathlib import Path
import json
import FreeCAD as A
import Part
OUT=Path(__file__).resolve().parent/'output'
doc=A.openDocument(str(OUT/'PanTilt_V9_HC-V760.FCStd'))
ex=A.newDocument('V9_STEP_export');objects=[];bounds=A.BoundBox()
for o in doc.Objects:
    if not hasattr(o,'Manufacturing'):continue
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement)
    bounds.add(s.BoundBox);p=ex.addObject('PartDesign::Feature',o.Name);p.Label=o.Label;p.Shape=s;objects.append(p)
Part.export(objects,str(OUT/'PanTilt_V9_assembly.step'))
s=Part.read(str(OUT/'PanTilt_V9_assembly.step'))
error=max(abs(getattr(s.BoundBox,k)-getattr(bounds,k)) for k in ('XMin','XMax','YMin','YMax','ZMin','ZMax'))
assert error<.001,(s.BoundBox,bounds)
report=json.loads((OUT/'geometry_validation.json').read_text())
report['step_export']={'global_bounds_match':True,'max_bounds_error_mm':error,'exported_components':len(objects)}
(OUT/'geometry_validation.json').write_text(json.dumps(report,indent=2))
print('STEP_GLOBAL_BOUNDS_PASS',error,flush=True)
