import os
import subprocess
import time

import FreeCAD as App
import FreeCADGui as Gui
import Part


ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT, "pantilt_hc_v760_nema17_gt2.FCStd")
SCREEN_DIR = os.path.join(ROOT, "screenshots")
REFERENCE_IMAGES = [
    "/home/user/Downloads/IMG_8292.jpeg",
    "/home/user/Downloads/IMG_8293.jpeg",
    "/home/user/Downloads/IMG_8294.jpeg",
]
os.makedirs(SCREEN_DIR, exist_ok=True)

for name in os.listdir(SCREEN_DIR):
    if name.lower().endswith(".png"):
        os.remove(os.path.join(SCREEN_DIR, name))

doc = App.openDocument(DOC_PATH)
Gui.setActiveDocument(doc.Name)
Gui.ActiveDocument = Gui.getDocument(doc.Name)
view = Gui.ActiveDocument.ActiveView

for container in doc.Objects:
    if container.TypeId == "App::Part":
        try:
            container.ViewObject.Visibility = True
        except Exception:
            pass

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
    "reference": (0.90, 0.08, 0.04),
    "clearance": (0.10, 0.34, 0.86),
}

TILT_PIVOT = App.Vector(10.3, 0, 180)
TILT_AXIS = App.Vector(0, 1, 0)
PAN_PIVOT = App.Vector(0, 0, 0)
PAN_AXIS = App.Vector(0, 0, 1)

shape_objects = []
for candidate in doc.Objects:
    if candidate.TypeId != "Part::Feature":
        continue
    try:
        if not candidate.Shape.isNull():
            shape_objects.append(candidate)
    except Exception:
        pass
original_shapes = {obj.Name: obj.Shape.copy() for obj in shape_objects}
print("SCREENSHOT_OBJECTS", len(shape_objects))


def role_for(obj):
    try:
        return obj.MaterialRole
    except Exception:
        return "printed"


def apply_style():
    for obj in shape_objects:
        role = role_for(obj)
        color = COLORS.get(role, COLORS["printed"])
        try:
            obj.ViewObject.ShapeColor = color
            if hasattr(obj.ViewObject, "LineColor"):
                obj.ViewObject.LineColor = color
            if hasattr(obj.ViewObject, "DisplayMode"):
                obj.ViewObject.DisplayMode = "Shaded"
            if hasattr(obj.ViewObject, "LineWidth"):
                obj.ViewObject.LineWidth = 1.0
            if role == "clearance":
                obj.ViewObject.Transparency = 72
            elif obj.Label == "CAMERA_HC_V760_body_placeholder":
                obj.ViewObject.Transparency = 12
            else:
                obj.ViewObject.Transparency = 0
        except Exception:
            pass


def restore_shapes():
    for obj in shape_objects:
        obj.Shape = original_shapes[obj.Name].copy()


def tilt_target(label):
    return label.startswith("TILT_ROTATING_") or label.startswith("CAMERA_")


def pan_target(label):
    return (
        label.startswith("PAN_ROTATING_")
        or label.startswith("TILT_ROTATING_")
        or label.startswith("CAMERA_")
    )


def set_pose(pan_angle=0, tilt_angle=0):
    restore_shapes()
    if tilt_angle:
        for obj in shape_objects:
            if tilt_target(obj.Label):
                shape = obj.Shape.copy()
                shape.rotate(TILT_PIVOT, TILT_AXIS, tilt_angle)
                obj.Shape = shape
    if pan_angle:
        for obj in shape_objects:
            if pan_target(obj.Label):
                shape = obj.Shape.copy()
                shape.rotate(PAN_PIVOT, PAN_AXIS, pan_angle)
                obj.Shape = shape
    doc.recompute()


def set_visibility(mode="normal", show_axes=False):
    for container in doc.Objects:
        if container.TypeId == "App::Part":
            try:
                container.ViewObject.Visibility = True
            except Exception:
                pass
    for obj in shape_objects:
        label = obj.Label
        visible = True
        if label.startswith("REFERENCE_") or label in ("CAMERA_nominal_COG", "CAMERA_optical_axis"):
            visible = show_axes
        if role_for(obj) == "clearance":
            visible = False

        if mode == "pan_focus":
            visible = (
                label.startswith("BASE_")
                or label.startswith("PAN_ROTATING_turntable")
                or label.startswith("PAN_ROTATING_bearing_adapter")
                or label.startswith("PAN_ROTATING_120T")
                or label.startswith("PAN_ROTATING_platform")
                or label.startswith("PAN_ROTATING_cable_guide")
            )
            if label.startswith("BASE_rubber"):
                visible = False
        elif mode == "tilt_focus":
            visible = (
                label.startswith("PAN_ROTATING_left_yoke")
                or label.startswith("PAN_ROTATING_right_yoke")
                or label.startswith("PAN_ROTATING_yoke_gusset")
                or label.startswith("PAN_ROTATING_left_608")
                or label.startswith("PAN_ROTATING_right_608")
                or label.startswith("PAN_ROTATING_left_bearing")
                or label.startswith("PAN_ROTATING_right_bearing")
                or label.startswith("PAN_ROTATING_tilt_")
                or label.startswith("TILT_ROTATING_")
            )
        elif mode == "direct_motor_focus":
            visible = (
                label == "PAN_ROTATING_right_yoke_motor_mount"
                or label.startswith("PAN_ROTATING_tilt_motor_")
                or label == "PAN_ROTATING_tilt_GT2_280mm_belt"
                or label == "TILT_ROTATING_one_piece_cradle_trunnions_80T"
            )
        elif mode == "motor_slots_focus":
            visible = label == "PAN_ROTATING_right_yoke_motor_mount"
        elif mode == "saddle_focus":
            visible = (
                label == "TILT_ROTATING_one_piece_cradle_trunnions_80T"
                or label.startswith("CAMERA_HC_V760_")
                or label == "CAMERA_nominal_COG"
            )
        elif mode == "service_focus":
            visible = (
                label == "TILT_ROTATING_one_piece_cradle_trunnions_80T"
                or label == "PAN_ROTATING_left_yoke"
                or label.startswith("PAN_ROTATING_left_608")
                or label.startswith("PAN_ROTATING_left_bearing")
                or label == "CAMERA_HC_V760_body_placeholder"
                or label == "CAMERA_flip_screen_clearance_open"
                or label == "CAMERA_HDMI_cable_clearance_20mm"
            )
        obj.ViewObject.Visibility = visible


def save_view(name, view_command, mode="normal", show_axes=False):
    Gui.Selection.clearSelection()
    set_visibility(mode, show_axes=show_axes)
    apply_style()
    if mode in ("saddle_focus", "service_focus"):
        for obj in shape_objects:
            if obj.Label == "CAMERA_HC_V760_body_placeholder":
                obj.ViewObject.Transparency = 78 if mode == "saddle_focus" else 62
            elif obj.Label == "CAMERA_HDMI_cable_clearance_20mm":
                obj.ViewObject.ShapeColor = (0.95, 0.36, 0.06)
                obj.ViewObject.LineColor = (0.95, 0.36, 0.06)
                obj.ViewObject.Transparency = 35
    Gui.updateGui()
    view_command()
    view.fitAll()
    Gui.updateGui()
    time.sleep(0.2)
    view.saveImage(os.path.join(SCREEN_DIR, name), 1600, 1200, "White")


def make_reference_comparison():
    filter_graph = (
        "[0:v]crop=900:900:350:180,scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[c0];"
        "[1:v]crop=1100:1000:250:70,scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[c1];"
        "[2:v]crop=900:900:350:180,scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[c2];"
        "[3:v]scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[r0];"
        "[4:v]scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[r1];"
        "[5:v]scale=560:560:force_original_aspect_ratio=decrease,"
        "pad=600:600:(ow-iw)/2:(oh-ih)/2:white[r2];"
        "[c0][c1][c2][r0][r1][r2]xstack=inputs=6:"
        "layout=0_0|600_0|1200_0|0_600|600_600|1200_600:fill=white[out]"
    )
    command = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-y",
        "-i",
        os.path.join(SCREEN_DIR, "01_isometric_v7.png"),
        "-i",
        os.path.join(SCREEN_DIR, "07_tilt_drive_focus_v7.png"),
        "-i",
        os.path.join(SCREEN_DIR, "02_front_v7.png"),
    ]
    for reference_path in REFERENCE_IMAGES:
        command.extend(["-i", reference_path])
    command.extend(
        [
            "-filter_complex",
            filter_graph,
            "-map",
            "[out]",
            "-frames:v",
            "1",
            "-update",
            "1",
            os.path.join(SCREEN_DIR, "11_reference_comparison_v7.png"),
        ]
    )
    subprocess.run(command, check=True)


def make_exploded():
    restore_shapes()
    for obj in shape_objects:
        label = obj.Label
        delta = App.Vector(0, 0, 0)
        if label.startswith("PAN_ROTATING_turntable") or label.startswith("PAN_ROTATING_bearing_adapter"):
            delta = App.Vector(0, 0, 18)
        elif label.startswith("PAN_ROTATING_120T") or label == "BASE_pan_GT2_252mm_belt":
            delta = App.Vector(0, 0, 8)
        elif label.startswith("PAN_ROTATING_left_yoke") or label.startswith("PAN_ROTATING_right_yoke"):
            delta = App.Vector(0, 0, 34)
        elif label.startswith("PAN_ROTATING_tilt_"):
            delta = App.Vector(0, -38, 34)
        elif label.startswith("PAN_ROTATING_left_608") or label.startswith("PAN_ROTATING_left_bearing"):
            delta = App.Vector(0, 28, 34)
        elif label.startswith("PAN_ROTATING_right_608") or label.startswith("PAN_ROTATING_right_bearing"):
            delta = App.Vector(0, -28, 34)
        elif label.startswith("TILT_ROTATING_") or label.startswith("CAMERA_"):
            delta = App.Vector(48, 0, 58)
        if delta.Length > 0:
            shape = obj.Shape.copy()
            shape.translate(delta)
            obj.Shape = shape
    doc.recompute()


def make_gt2_profile_closeup():
    restore_shapes()
    set_visibility("normal", show_axes=False)
    target = next(
        obj for obj in shape_objects
        if obj.Label == "TILT_ROTATING_one_piece_cradle_trunnions_80T"
    )
    for obj in shape_objects:
        obj.ViewObject.Visibility = obj == target
    # Keep only the 10 mm toothed face so the flanges cannot hide the 2MR outline.
    detail_box = Part.makeBox(67, 9.8, 66, App.Vector(-23, -50.7, 147))
    target.Shape = target.Shape.common(detail_box)
    doc.recompute()


apply_style()
print("SCREENSHOT_STAGE", "styled")
view.setAxisCross(False)
Gui.runCommand("Std_DrawStyle", 0)

set_pose(pan_angle=-18, tilt_angle=0)
print("SCREENSHOT_STAGE", "pose_01")
save_view("01_isometric_v7.png", view.viewIsometric)
print("SCREENSHOT_STAGE", "saved_01")

set_pose()
save_view("02_front_v7.png", view.viewFront)
print("SCREENSHOT_STAGE", "saved_02")
save_view("03_side_v7.png", view.viewRight)
print("SCREENSHOT_STAGE", "saved_03")
save_view("04_top_v7.png", view.viewTop)
print("SCREENSHOT_STAGE", "saved_04")

make_exploded()
save_view("05_exploded_v7.png", view.viewIsometric)
print("SCREENSHOT_STAGE", "saved_05")

set_pose()
save_view("06_pan_drive_focus_v7.png", view.viewTop, mode="pan_focus")
print("SCREENSHOT_STAGE", "saved_06")
save_view("07_tilt_drive_focus_v7.png", view.viewIsometric, mode="tilt_focus", show_axes=True)
print("SCREENSHOT_STAGE", "saved_07")

set_pose(pan_angle=-18, tilt_angle=60)
save_view("08_tilt_plus60_v7.png", view.viewIsometric, show_axes=True)

set_pose(pan_angle=-18, tilt_angle=-60)
save_view("09_tilt_minus60_v7.png", view.viewIsometric, show_axes=True)

set_pose(pan_angle=45, tilt_angle=18)
save_view("10_pan45_tilt18_v7.png", view.viewIsometric)

make_reference_comparison()
print("SCREENSHOT_STAGE", "saved_11_comparison")

make_gt2_profile_closeup()
apply_style()
view.viewFront()
view.fitAll()
Gui.updateGui()
time.sleep(0.2)
view.saveImage(
    os.path.join(SCREEN_DIR, "12_gt2_2mr_profile_closeup_v7.png"),
    1600,
    1200,
    "White",
)
print("SCREENSHOT_STAGE", "saved_12_gt2_profile")

set_pose()
save_view("13_direct_tilt_motor_mount_v7.png", view.viewIsometric, mode="direct_motor_focus")
print("SCREENSHOT_STAGE", "saved_13_direct_motor")
save_view("14_integrated_nema17_tension_slots_v7.png", view.viewFront, mode="motor_slots_focus")
print("SCREENSHOT_STAGE", "saved_14_motor_slots")

set_pose()
save_view("15_short_camera_saddle_v7.png", view.viewTop, mode="saddle_focus", show_axes=True)
print("SCREENSHOT_STAGE", "saved_15_short_saddle")
save_view("16_open_lcd_hdmi_clearance_v7.png", view.viewRight, mode="service_focus")
print("SCREENSHOT_STAGE", "saved_16_service_clearance")

restore_shapes()
set_visibility("normal", show_axes=False)
doc.recompute()
doc.saveAs(DOC_PATH)
print("WROTE_SCREENSHOTS", SCREEN_DIR)
App.closeDocument(doc.Name)
try:
    Gui.getMainWindow().close()
except Exception:
    pass
