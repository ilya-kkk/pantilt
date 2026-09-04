import os
import time
import sys

import FreeCAD as App
import FreeCADGui as Gui
import Part

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT, "pantilt_hc_v760_nema17_gt2.FCStd")
OUT = os.path.join(ROOT, "screenshots", "section_xz_pan_bearing_node_v8.png")

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

# Cut plane y = 0 (through the pan axis); keep the y <= 0 half, camera at +Y.
half_space = Part.makeBox(600, 300, 450, App.Vector(-300, -300, -25))
# Close-up node box around the pan bearing entry:
# x -60..60, z 38..96 (120T gear z 47..57, skirt, 51107 stack 65..77,
# 608 + journal + seats, square platform 76..83).
node_box = Part.makeBox(120, 30, 58, App.Vector(-60, -30, 38))

for obj in doc.Objects:
    if obj.TypeId != "Part::Feature" or not hasattr(obj, "Shape") or obj.Shape.isNull():
        continue
    label = obj.Label
    role = getattr(obj, "MaterialRole", "printed")
    if label.startswith("REFERENCE_") or label in hidden_labels or role == "clearance":
        obj.ViewObject.Visibility = False
        continue
    shape = obj.Shape.copy().common(half_space)
    shape = shape.common(node_box)
    if shape.isNull():
        obj.ViewObject.Visibility = False
        continue
    obj.Shape = shape
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

App.closeDocument(doc.Name)
try:
    Gui.getMainWindow().close()
except Exception:
    pass
sys.exit(0)
