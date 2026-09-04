import os
import time

import FreeCAD as App
import FreeCADGui as Gui
import Part

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT, "pantilt_hc_v760_nema17_gt2.FCStd")
OUT = os.path.join(ROOT, "screenshots", "section_xz_through_pan_axis_v8.png")

COLORS = {
    "printed": (0.66, 0.68, 0.70),
    "printed_dark": (0.24, 0.27, 0.29),
    "motor": (0.035, 0.04, 0.045),
    "belt": (0.012, 0.014, 0.016),
    "bearing": (0.43, 0.46, 0.49),
    "steel": (0.64, 0.67, 0.70),
    "pulley": (0.30, 0.33, 0.36),
    "rubber": (0.04, 0.045, 0.05),
    "camera": (0.055, 0.065, 0.075),
    "camera_detail": (0.12, 0.14, 0.15),
}

doc = App.openDocument(DOC_PATH)
Gui.setActiveDocument(doc.Name)
gui_doc = Gui.getDocument(doc.Name)
Gui.ActiveDocument = gui_doc

hidden_labels = {
    "CAMERA_flip_screen_clearance_closed",
    "CAMERA_nominal_COG",
    "CAMERA_optical_axis",
}

# Section plane y = 0: passes exactly through the pan axis (z axis at origin),
# and through the tilt axis (x=10.3, z=180). Keep the y <= 0 half (the
# tilt-drive / pan-motor side) and render from the rear (+Y camera, looking
# along -Y) so the flat cut face at y = 0 faces the viewer and the cut
# features (608, journal, 51107 stack, 120T/80T teeth, trunnions, motors,
# belts) are visible behind it.
half_space = Part.makeBox(600, 300, 450, App.Vector(-300, -300, -25))

shape_objects = []
for obj in doc.Objects:
    if obj.TypeId != "Part::Feature" or not hasattr(obj, "Shape") or obj.Shape.isNull():
        continue
    shape_objects.append(obj)

for obj in shape_objects:
    label = obj.Label
    role = getattr(obj, "MaterialRole", "printed")
    skip = (
        label.startswith("REFERENCE_")
        or label in hidden_labels
        or role == "clearance"
    )
    if skip:
        obj.ViewObject.Visibility = False
        continue
    obj.Shape = obj.Shape.copy().common(half_space)
    if role in COLORS:
        obj.ViewObject.ShapeColor = COLORS[role]
        obj.ViewObject.LineColor = COLORS[role]
    obj.ViewObject.DisplayMode = "Flat Lines"
    obj.ViewObject.Transparency = 0
    obj.ViewObject.Visibility = True

doc.recompute()
Gui.Selection.clearSelection()
view = gui_doc.ActiveView
view.setAxisCross(False)
Gui.runCommand("Std_DrawStyle", 0)
view.viewRear()
view.fitAll()
Gui.updateGui()
time.sleep(0.4)
view.saveImage(OUT, 1600, 1200, "White")
print("WROTE_SECTION", OUT)

import sys

App.closeDocument(doc.Name)
try:
    Gui.getMainWindow().close()
except Exception:
    pass
sys.exit(0)
