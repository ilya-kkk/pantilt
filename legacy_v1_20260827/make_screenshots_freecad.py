import os
import time

import FreeCAD as App
import FreeCADGui as Gui


ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT, "pantilt_hc_v760_nema17_gt2.FCStd")
SCREEN_DIR = os.path.join(ROOT, "screenshots")
os.makedirs(SCREEN_DIR, exist_ok=True)

for name in os.listdir(SCREEN_DIR):
    if name.lower().endswith(".png"):
        os.remove(os.path.join(SCREEN_DIR, name))

doc = App.openDocument(DOC_PATH)
Gui.setActiveDocument(doc.Name)
Gui.ActiveDocument = Gui.getDocument(doc.Name)

COLORS = {
    "aluminum": (0.72, 0.74, 0.76, 0.0),
    "plastic": (0.12, 0.32, 0.85, 0.0),
    "bearing": (0.45, 0.49, 0.53, 0.0),
    "dark": (0.03, 0.035, 0.04, 0.0),
    "brass": (0.93, 0.62, 0.18, 0.0),
    "belt": (0.005, 0.005, 0.006, 0.0),
    "camera": (0.08, 0.12, 0.18, 0.0),
    "red": (0.95, 0.08, 0.04, 0.0),
}


def style_for(label):
    low = label.lower()
    if "camera_wire" in low:
        return COLORS["camera"], 65, "Wireframe"
    if "axis" in low or "cog" in low:
        return COLORS["red"], 0, "Shaded"
    if "belt" in low:
        return COLORS["belt"], 0, "Shaded"
    if "pulley" in low or "tooth" in low:
        return COLORS["brass"], 0, "Shaded"
    if "bearing" in low or "shaft" in low:
        return COLORS["bearing"], 0, "Shaded"
    if "nema17" in low or "motor_" in low:
        return COLORS["dark"], 0, "Shaded"
    if "tilt_rotating" in low:
        return COLORS["plastic"], 0, "Shaded"
    return COLORS["aluminum"], 0, "Shaded"


def apply_visibility(mode):
    for obj in doc.Objects:
        if not hasattr(obj, "Shape"):
            continue
        visible = True
        low = obj.Label.lower()
        if mode == "pan_section":
            visible = low.startswith(("base_", "pan_")) or "panaxis" in low
        elif mode == "tilt_section":
            visible = low.startswith(("tilt_", "camera_")) or "tiltaxis" in low or "cameraopticalaxis" in low or "cog" in low
        obj.Visibility = visible
        try:
            obj.ViewObject.Visibility = visible
            c, tr, display = style_for(obj.Label)
            obj.ViewObject.ShapeColor = c
            obj.ViewObject.Transparency = tr
            obj.ViewObject.DisplayMode = display
            if display == "Wireframe":
                obj.ViewObject.LineColor = c
                obj.ViewObject.LineWidth = 2.0
        except Exception:
            pass


def save_view(name, view_cmd, mode="normal"):
    apply_visibility(mode)
    Gui.updateGui()
    view_cmd()
    view.fitAll()
    Gui.updateGui()
    time.sleep(0.25)
    view.saveImage(os.path.join(SCREEN_DIR, name), 1600, 1200, "White")


view = Gui.ActiveDocument.ActiveView
view.setAxisCross(True)
Gui.runCommand("Std_DrawStyle", 0)

save_view("01_isometric.png", view.viewIsometric)
save_view("02_front.png", view.viewFront)
save_view("03_side.png", view.viewRight)
save_view("04_top.png", view.viewTop)

saved = {}
for obj in doc.Objects:
    if hasattr(obj, "Placement"):
        saved[obj.Name] = App.Placement(obj.Placement)
        low = obj.Label.lower()
        if low.startswith("pan_rotating") or low.startswith("tilt_") or low.startswith("camera"):
            obj.Placement.move(App.Vector(0, 0, 38))
        if low.startswith("tilt_rotating") or low.startswith("camera"):
            obj.Placement.move(App.Vector(70, 0, 28))
        if "nema17" in low or "motor_gt2" in low:
            obj.Placement.move(App.Vector(-35, 0, 0))
doc.recompute()
save_view("05_exploded.png", view.viewIsometric)
for obj in doc.Objects:
    if obj.Name in saved:
        obj.Placement = saved[obj.Name]
doc.recompute()

save_view("06_pan_bearing_section_focus.png", view.viewFront, mode="pan_section")
save_view("07_tilt_bearing_section_focus.png", view.viewRight, mode="tilt_section")

apply_visibility("normal")
doc.recompute()
doc.saveAs(DOC_PATH)
print("WROTE_SCREENSHOTS", SCREEN_DIR)
App.closeDocument(doc.Name)
try:
    Gui.getMainWindow().close()
except Exception:
    pass
