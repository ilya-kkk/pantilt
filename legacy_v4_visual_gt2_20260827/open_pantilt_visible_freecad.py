import os

import FreeCAD as App
import FreeCADGui as Gui


ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT, "pantilt_hc_v760_nema17_gt2.FCStd")

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

for obj in doc.Objects:
    if obj.TypeId == "App::Part":
        obj.ViewObject.Visibility = True
        continue
    if obj.TypeId == "Spreadsheet::Sheet":
        obj.ViewObject.Visibility = False
        continue
    if obj.TypeId != "Part::Feature":
        continue

    obj.ViewObject.Visibility = not (
        obj.Label.startswith("REFERENCE_") or obj.Label in hidden_labels
    )
    role = getattr(obj, "MaterialRole", "printed")
    if role in COLORS:
        obj.ViewObject.ShapeColor = COLORS[role]
        obj.ViewObject.LineColor = COLORS[role]
    obj.ViewObject.DisplayMode = "Shaded"
    obj.ViewObject.Transparency = 12 if obj.Label == "CAMERA_HC_V760_body_placeholder" else 0

Gui.Selection.clearSelection()
view = gui_doc.ActiveView
view.setAxisCross(False)
view.viewIsometric()
view.fitAll()
doc.recompute()
Gui.updateGui()
doc.saveAs(DOC_PATH)
