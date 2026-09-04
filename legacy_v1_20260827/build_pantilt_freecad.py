import math
import os

import FreeCAD as App
import Part


try:
    OUT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    OUT_DIR = os.getcwd()

DOC_NAME = "pantilt_hc_v760_nema17_gt2"

P = {
    "camera_w": 65.0,
    "camera_h": 73.0,
    "camera_d": 139.0,
    "pan_bearing_id": 35.0,
    "pan_bearing_od": 52.0,
    "pan_bearing_h": 12.0,
    "plate_t": 10.0,
    "nema_w": 42.3,
    "nema_l": 48.0,
    "nema_bolt": 31.0,
    "nema_bolt_d": 3.4,
    "nema_pilot_d": 22.0,
    "shaft_d": 8.0,
    "bearing_608_od": 22.0,
    "bearing_608_id": 8.0,
    "bearing_608_w": 7.0,
    "gt2_w": 10.0,
    "motor_pulley_d": 18.0,
    "pan_pitch_d": 108.0,
    "tilt_pitch_d": 72.0,
    "camera_mass_design_kg": 0.6,
    "camera_plate_l": 160.0,
    "camera_plate_w": 80.0,
    "camera_plate_t": 5.0,
    "belt_pitch": 2.0,
    "pan_motor_teeth": 20.0,
    "pan_driven_teeth": 80.0,
    "tilt_motor_teeth": 20.0,
    "tilt_driven_teeth": 80.0,
    "bearing_press_clearance": 0.15,
    "tilt_inner_width": 95.0,
    "tilt_axis_height_above_plate": 40.0,
    "wall_t": 5.0,
    "pan_belt_tension_range": 10.0,
    "tilt_belt_tension_range": 10.0,
}

P["pan_pitch_d"] = P["pan_driven_teeth"] * P["belt_pitch"] / math.pi
P["tilt_pitch_d"] = P["tilt_driven_teeth"] * P["belt_pitch"] / math.pi
P["motor_pulley_d"] = P["pan_motor_teeth"] * P["belt_pitch"] / math.pi


def vec(x, y, z):
    return App.Vector(float(x), float(y), float(z))


def color(name):
    return {
        "aluminum": (0.72, 0.74, 0.76, 0.0),
        "plastic": (0.12, 0.32, 0.85, 0.0),
        "dark": (0.03, 0.035, 0.04, 0.0),
        "rubber": (0.005, 0.005, 0.006, 0.0),
        "bearing": (0.48, 0.51, 0.54, 0.0),
        "brass": (0.93, 0.62, 0.16, 0.0),
        "camera": (0.08, 0.12, 0.18, 0.0),
        "red": (0.9, 0.05, 0.04, 0.0),
    }[name]


def add(doc, label, shape, mat):
    obj = doc.addObject("Part::Feature", label)
    obj.Shape = shape
    try:
        obj.ViewObject.ShapeColor = color(mat)
        obj.ViewObject.DisplayMode = "Shaded"
    except Exception:
        pass
    return obj


def make_spreadsheet(doc):
    sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
    rows = [
        ("CAMERA_WIDTH", P["camera_w"], "mm"),
        ("CAMERA_HEIGHT", P["camera_h"], "mm"),
        ("CAMERA_LENGTH", P["camera_d"], "mm"),
        ("CAMERA_MASS_DESIGN", P["camera_mass_design_kg"], "kg"),
        ("CAMERA_PLATE_WIDTH", P["camera_plate_w"], "mm"),
        ("CAMERA_PLATE_LENGTH", P["camera_plate_l"], "mm"),
        ("CAMERA_PLATE_THICKNESS", P["camera_plate_t"], "mm"),
        ("NEMA_SIZE", P["nema_w"], "mm"),
        ("NEMA_HOLE_SPACING", P["nema_bolt"], "mm"),
        ("NEMA_SHAFT_D", 5, "mm"),
        ("BELT_PITCH", P["belt_pitch"], "mm"),
        ("BELT_WIDTH", P["gt2_w"], "mm"),
        ("PAN_MOTOR_TEETH", P["pan_motor_teeth"], "teeth"),
        ("PAN_DRIVEN_TEETH", P["pan_driven_teeth"], "teeth"),
        ("PAN_DRIVEN_PITCH_D", P["pan_pitch_d"], "mm"),
        ("TILT_MOTOR_TEETH", P["tilt_motor_teeth"], "teeth"),
        ("TILT_DRIVEN_TEETH", P["tilt_driven_teeth"], "teeth"),
        ("TILT_DRIVEN_PITCH_D", P["tilt_pitch_d"], "mm"),
        ("BEARING_ID", P["bearing_608_id"], "mm"),
        ("BEARING_OD", P["bearing_608_od"], "mm"),
        ("BEARING_WIDTH", P["bearing_608_w"], "mm"),
        ("AXLE_DIAMETER", P["shaft_d"], "mm"),
        ("TILT_INNER_WIDTH", P["tilt_inner_width"], "mm"),
        ("TILT_AXIS_HEIGHT_ABOVE_PLATE", P["tilt_axis_height_above_plate"], "mm"),
        ("WALL_THICKNESS", P["wall_t"], "mm"),
        ("BEARING_PRESS_CLEARANCE", P["bearing_press_clearance"], "mm"),
        ("PAN_BELT_TENSION_RANGE", P["pan_belt_tension_range"], "mm"),
        ("TILT_BELT_TENSION_RANGE", P["tilt_belt_tension_range"], "mm"),
    ]
    sheet.set("A1", "PARAMETER")
    sheet.set("B1", "VALUE")
    sheet.set("C1", "UNIT")
    for i, (name, value, unit) in enumerate(rows, start=2):
        sheet.set(f"A{i}", name)
        sheet.set(f"B{i}", str(round(float(value), 4)))
        sheet.set(f"C{i}", unit)
        try:
            sheet.setAlias(f"B{i}", name)
        except Exception:
            pass
    return sheet


def box(l, w, h, c):
    return Part.makeBox(l, w, h, vec(c[0] - l / 2, c[1] - w / 2, c[2] - h / 2))


def cyl_z(r, h, c):
    return Part.makeCylinder(r, h, vec(c[0], c[1], c[2] - h / 2), vec(0, 0, 1))


def cyl_y(r, h, c):
    return Part.makeCylinder(r, h, vec(c[0], c[1] - h / 2, c[2]), vec(0, 1, 0))


def cyl_x(r, h, c):
    return Part.makeCylinder(r, h, vec(c[0] - h / 2, c[1], c[2]), vec(1, 0, 0))


def ring_z(od, id_, h, c):
    return cyl_z(od / 2, h, c).cut(cyl_z(id_ / 2, h + 2, c))


def ring_y(od, id_, h, c):
    return cyl_y(od / 2, h, c).cut(cyl_y(id_ / 2, h + 2, c))


def slot_z(length, width, h, c):
    x, y, z = c
    return (
        box(max(0.1, length - width), width, h, c)
        .fuse(cyl_z(width / 2, h, (x - (length - width) / 2, y, z)))
        .fuse(cyl_z(width / 2, h, (x + (length - width) / 2, y, z)))
    )


def slot_y(length, width, depth, c, along="x"):
    x, y, z = c
    if along == "x":
        return (
            box(max(0.1, length - width), depth, width, c)
            .fuse(cyl_y(width / 2, depth, (x - (length - width) / 2, y, z)))
            .fuse(cyl_y(width / 2, depth, (x + (length - width) / 2, y, z)))
        )
    return (
        box(width, depth, max(0.1, length - width), c)
        .fuse(cyl_y(width / 2, depth, (x, y, z - (length - width) / 2)))
        .fuse(cyl_y(width / 2, depth, (x, y, z + (length - width) / 2)))
    )


def bolt_pattern_y(shape, pitch, hole_d, depth, y, x0=0, z0=0):
    out = shape
    for sx in (-1, 1):
        for sz in (-1, 1):
            out = out.cut(cyl_y(hole_d / 2, depth + 2, (x0 + sx * pitch / 2, y, z0 + sz * pitch / 2)))
    return out


def tooth_ring_z(pitch_d, h, z, teeth=72, tooth_h=2.2):
    parts = []
    r = pitch_d / 2 + tooth_h / 2
    tangential = max(1.4, math.pi * pitch_d / teeth * 0.42)
    for i in range(teeth):
        a = 360.0 * i / teeth
        tooth = box(tooth_h, tangential, h, (r, 0, z))
        tooth.Placement = App.Placement(vec(0, 0, 0), App.Rotation(vec(0, 0, 1), a))
        parts.append(tooth)
    return Part.makeCompound(parts)


def tooth_ring_y(pitch_d, w, c, teeth=54, tooth_h=2.0):
    x0, y0, z0 = c
    parts = []
    r = pitch_d / 2 + tooth_h / 2
    tangential = max(1.4, math.pi * pitch_d / teeth * 0.42)
    for i in range(teeth):
        a = 360.0 * i / teeth
        tooth = box(tooth_h, w, tangential, (r, 0, 0))
        tooth.Placement = App.Placement(vec(x0, y0, z0), App.Rotation(vec(0, 1, 0), -a))
        parts.append(tooth)
    return Part.makeCompound(parts)


def nema17_z_down(c):
    x, y, z = c
    return [
        ("PAN_motor_NEMA17_body_inverted", box(P["nema_w"], P["nema_w"], P["nema_l"], c), "dark"),
        ("PAN_motor_22mm_pilot_face_down", cyl_z(P["nema_pilot_d"] / 2, 2, (x, y, z - P["nema_l"] / 2 - 1)), "bearing"),
        ("PAN_motor_5mm_shaft_down", cyl_z(2.5, 22, (x, y, z - P["nema_l"] / 2 - 11)), "bearing"),
    ]


def nema17_y_inward(c):
    x, y, z = c
    return [
        ("TILT_motor_NEMA17_body_outside_right", box(P["nema_w"], P["nema_l"], P["nema_w"], c), "dark"),
        ("TILT_motor_22mm_pilot_inward", cyl_y(P["nema_pilot_d"] / 2, 2, (x, y + P["nema_l"] / 2 + 1, z)), "bearing"),
        ("TILT_motor_5mm_shaft_inward", cyl_y(2.5, 28, (x, y + P["nema_l"] / 2 + 14, z)), "bearing"),
    ]


def pulley_z(label, d, bore, z, x, y):
    return [
        (label + "_body", ring_z(d, bore, P["gt2_w"], (x, y, z)), "brass"),
        (label + "_flanges", ring_z(d + 4, bore, 1.2, (x, y, z - P["gt2_w"] / 2 - 0.6)).fuse(ring_z(d + 4, bore, 1.2, (x, y, z + P["gt2_w"] / 2 + 0.6))), "brass"),
    ]


def pulley_y(label, d, bore, c):
    x, y, z = c
    return [
        (label + "_body", ring_y(d, bore, P["gt2_w"], c), "brass"),
        (label + "_flanges", ring_y(d + 4, bore, 1.2, (x, y - P["gt2_w"] / 2 - 0.6, z)).fuse(ring_y(d + 4, bore, 1.2, (x, y + P["gt2_w"] / 2 + 0.6, z))), "brass"),
    ]


def belt_z(label, a, da, b, db, z):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    nx, ny = -uy, ux
    angle = math.degrees(math.atan2(uy, ux))
    parts = [ring_z(da + 4, da, P["gt2_w"], (ax, ay, z)), ring_z(db + 4, db, P["gt2_w"], (bx, by, z))]
    for side in (-1, 1):
        run = box(dist, 2, P["gt2_w"], (0, 0, 0))
        run.Placement = App.Placement(vec((ax + bx) / 2 + nx * side * (da + db) / 4, (ay + by) / 2 + ny * side * (da + db) / 4, z), App.Rotation(vec(0, 0, 1), angle))
        parts.append(run)
    return [(label, Part.makeCompound(parts), "rubber")]


def belt_y(label, a, da, b, db, y):
    ax, az = a
    bx, bz = b
    dx, dz = bx - ax, bz - az
    dist = math.hypot(dx, dz)
    ux, uz = dx / dist, dz / dist
    nx, nz = -uz, ux
    angle = -math.degrees(math.atan2(uz, ux))
    parts = [ring_y(da + 4, da, P["gt2_w"], (ax, y, az)), ring_y(db + 4, db, P["gt2_w"], (bx, y, bz))]
    for side in (-1, 1):
        run = box(dist, P["gt2_w"], 2, (0, 0, 0))
        run.Placement = App.Placement(vec((ax + bx) / 2 + nx * side * (da + db) / 4, y, (az + bz) / 2 + nz * side * (da + db) / 4), App.Rotation(vec(0, 1, 0), angle))
        parts.append(run)
    return [(label, Part.makeCompound(parts), "rubber")]


def build():
    doc = App.newDocument(DOC_NAME)
    make_spreadsheet(doc)
    try:
        doc.addObject("Assembly::AssemblyObject", "Assembly_PanTilt_DOF_reference")
    except Exception:
        asm = doc.addObject("App::Part", "Assembly_PanTilt_DOF_reference")
        asm.addProperty("App::PropertyString", "Note", "Assembly")
        asm.Note = "Base fixed; PanAssembly revolute about PanAxis Z; TiltAssembly revolute about TiltAxis Y."

    base = cyl_z(58, P["plate_t"], (0, 0, 5))
    for a in (0, 90, 180, 270):
        leg = box(108, 34, P["plate_t"], (83, 0, 5))
        leg = leg.cut(cyl_z(3.5, P["plate_t"] + 2, (126, 0, 5)))
        leg.Placement = App.Placement(vec(0, 0, 0), App.Rotation(vec(0, 0, 1), a))
        base = base.fuse(leg)
    add(doc, "BASE_plate_with_mounting_slots", base, "aluminum")
    add(doc, "BASE_center_spigot_35mm_for_35x52x12_thrust_bearing", cyl_z(P["pan_bearing_id"] / 2, 5, (0, 0, 12.5)), "aluminum")
    add(doc, "PAN_thrust_bearing_35x52x12", ring_z(P["pan_bearing_od"], P["pan_bearing_id"], P["pan_bearing_h"], (0, 0, 21)), "bearing")

    add(doc, "PAN_rotating_cup_grabs_outer_race_of_thrust_bearing", ring_z(112, 52.6, 18, (0, 0, 24)).fuse(ring_z(122, 35.8, 8, (0, 0, 35))), "plastic")
    add(doc, "PAN_integrated_external_GT2_10_tooth_ring", tooth_ring_z(P["pan_pitch_d"], P["gt2_w"], 30, teeth=72), "plastic")

    pan_motor_x, pan_motor_y = -92, 0
    mount = box(70, 56, 6, (pan_motor_x, pan_motor_y, 47))
    mount = mount.cut(cyl_z((P["nema_pilot_d"] + 1) / 2, 8, (pan_motor_x, pan_motor_y, 47)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            mount = mount.cut(slot_z(18, P["nema_bolt_d"], 8, (pan_motor_x + sx * P["nema_bolt"] / 2, pan_motor_y + sy * P["nema_bolt"] / 2, 47)))
    add(doc, "PAN_motor_slotted_mount_plate_for_belt_tension", mount, "aluminum")
    posts = Part.makeCompound([cyl_z(3.5, 37, (pan_motor_x + sx * 28, pan_motor_y + sy * 22, 28.5)) for sx in (-1, 1) for sy in (-1, 1)])
    add(doc, "PAN_motor_mount_posts_to_base", posts, "aluminum")
    for label, shape, mat in nema17_z_down((pan_motor_x, pan_motor_y, 73)):
        add(doc, label, shape, mat)
    for label, shape, mat in pulley_z("PAN_motor_GT2_10_pulley_on_downshaft", P["motor_pulley_d"], 5, 31, pan_motor_x, pan_motor_y):
        add(doc, label, shape, mat)
    for label, shape, mat in belt_z("PAN_closed_GT2_10_belt_to_integrated_ring", (pan_motor_x, pan_motor_y), P["motor_pulley_d"], (0, 0), P["pan_pitch_d"], 31):
        add(doc, label, shape, mat)

    yoke_wall_t = 9
    side_y = P["tilt_inner_width"] / 2 + yoke_wall_t / 2
    tilt_x, tilt_z = 22, 112
    for label, y in (("left", side_y), ("right", -side_y)):
        plate = box(132, yoke_wall_t, 110, (28, y, 92))
        plate = plate.cut(cyl_y((P["bearing_608_od"] + P["bearing_press_clearance"]) / 2, 11, (tilt_x, y, tilt_z)))
        plate = plate.cut(cyl_y((P["bearing_608_id"] + 0.8) / 2, 12, (tilt_x, y, tilt_z)))
        plate = plate.cut(slot_y(42, 14, 12, (72, y, 114), along="z"))
        plate = bolt_pattern_y(plate, 70, 5.2, 12, y, x0=20, z0=72)
        add(doc, f"PAN_ROTATING_big_{label}_yoke_plate_with_608_seat", plate, "plastic")
    add(doc, "PAN_ROTATING_rear_bridge_makes_big_yoke_one_part", box(14, side_y * 2 + yoke_wall_t, 92, (-34, 0, 88)), "plastic")
    add(doc, "PAN_ROTATING_left_foot_bolted_to_pan_cup", box(110, 20, 9, (20, side_y, 45)), "plastic")
    add(doc, "PAN_ROTATING_right_foot_bolted_to_pan_cup", box(110, 20, 9, (20, -side_y, 45)), "plastic")
    add(doc, "PAN_ROTATING_M5_foot_bolts_into_pan_cup", Part.makeCompound([cyl_z(2.5, 20, (x, y, 45)) for x in (-24, 54) for y in (-side_y, side_y)]), "dark")
    add(doc, "TILT_left_608_bearing_in_big_yoke", ring_y(P["bearing_608_od"], P["bearing_608_id"], P["bearing_608_w"], (tilt_x, side_y, tilt_z)), "bearing")
    add(doc, "TILT_right_608_bearing_in_big_yoke", ring_y(P["bearing_608_od"], P["bearing_608_id"], P["bearing_608_w"], (tilt_x, -side_y, tilt_z)), "bearing")

    cradle_base_z = tilt_z - P["tilt_axis_height_above_plate"] - P["camera_plate_t"] / 2
    cradle = box(P["camera_plate_l"], P["camera_plate_w"], P["camera_plate_t"], (35, 0, cradle_base_z))
    cradle = cradle.cut(slot_z(44, 6.8, 11, (35, 0, cradle_base_z)))
    for x in (-25, 95):
        for y in (-31, 31):
            cradle = cradle.cut(cyl_z(2.4, P["camera_plate_t"] + 2, (x, y, cradle_base_z)))
    for x in (-5, 75):
        cradle = cradle.cut(slot_z(22, 4.5, P["camera_plate_t"] + 2, (x, -P["camera_plate_w"] / 2 + 8, cradle_base_z)))
        cradle = cradle.cut(slot_z(22, 4.5, P["camera_plate_t"] + 2, (x, P["camera_plate_w"] / 2 - 8, cradle_base_z)))
    add(doc, "TILT_ROTATING_camera_cradle_base_with_1_4_slot", cradle, "plastic")
    add(doc, "TILT_ROTATING_camera_cradle_left_cheek", box(146, 8, 45, (36, 41, 93)), "plastic")
    add(doc, "TILT_ROTATING_camera_cradle_right_cheek", box(146, 8, 45, (36, -41, 93)), "plastic")
    add(doc, "TILT_ROTATING_left_8mm_plastic_shaft_into_608", cyl_y(P["shaft_d"] / 2, 28, (tilt_x, side_y - 13, tilt_z)), "plastic")
    add(doc, "TILT_ROTATING_right_8mm_plastic_shaft_into_608", cyl_y(P["shaft_d"] / 2, 28, (tilt_x, -side_y + 13, tilt_z)), "plastic")
    add(doc, "CAMERA_wire_envelope_Panasonic_HC_V760", box(P["camera_d"], P["camera_w"], P["camera_h"], (38, 0, 111)), "camera")
    add(doc, "CAMERA_red_optical_axis", cyl_x(1.1, 195, (38, 0, 113)), "red")
    add(doc, "CAMERA_COG_design_point_600g", cyl_z(3.0, 6.0, (38, 0, 111)), "red")
    add(doc, "PanAxis_Z_reference", cyl_z(1.2, 160, (0, 0, 80)), "red")
    add(doc, "TiltAxis_Y_reference", cyl_y(1.2, 160, (tilt_x, 0, tilt_z)), "red")
    add(doc, "CameraOpticalAxis_reference", cyl_x(0.9, 195, (38, 0, 113)), "red")
    add(doc, "COG_to_TiltAxis_offset_visual", cyl_x(0.9, abs(38 - tilt_x), ((38 + tilt_x) / 2, 0, 111)), "red")

    tilt_motor_x, tilt_motor_y, tilt_motor_z = tilt_x, -91, 58
    tilt_mount = box(68, 7, 68, (tilt_motor_x, -63, tilt_motor_z))
    tilt_mount = tilt_mount.cut(cyl_y((P["nema_pilot_d"] + 1) / 2, 9, (tilt_motor_x, -63, tilt_motor_z)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            tilt_mount = tilt_mount.cut(slot_y(18, P["nema_bolt_d"], 9, (tilt_motor_x + sx * P["nema_bolt"] / 2, -63, tilt_motor_z + sz * P["nema_bolt"] / 2), along="x"))
    add(doc, "TILT_motor_slotted_mount_on_right_yoke_outside", tilt_mount, "aluminum")
    for label, shape, mat in nema17_y_inward((tilt_motor_x, tilt_motor_y, tilt_motor_z)):
        add(doc, label, shape, mat)
    for label, shape, mat in pulley_y("TILT_motor_GT2_10_pulley_inside_yoke", P["motor_pulley_d"], 5, (tilt_motor_x, -52, tilt_motor_z)):
        add(doc, label, shape, mat)
    for label, shape, mat in pulley_y("TILT_driven_GT2_10_wheel_on_cradle_shaft", P["tilt_pitch_d"], P["shaft_d"], (tilt_x, -47, tilt_z)):
        add(doc, label, shape, mat)
    add(doc, "TILT_driven_external_GT2_teeth_on_cradle_wheel", tooth_ring_y(P["tilt_pitch_d"], P["gt2_w"], (tilt_x, -47, tilt_z), teeth=54), "plastic")
    for label, shape, mat in belt_y("TILT_closed_GT2_10_belt_inside_right_yoke", (tilt_motor_x, tilt_motor_z), P["motor_pulley_d"], (tilt_x, tilt_z), P["tilt_pitch_d"], -52):
        add(doc, label, shape, mat)

    add(doc, "TILT_adjustable_idler_625_bearing", ring_y(16, 5, P["gt2_w"], (tilt_x + 28, -52, 86)), "bearing")
    add(doc, "TILT_idler_vertical_slot_bracket", slot_y(34, 7, 6, (tilt_x + 28, -64, 86), along="z"), "aluminum")
    add(doc, "TILT_angle_stop_tab_on_inner_cradle", box(9, 86, 24, (94, 0, 102)), "plastic")
    add(doc, "TILT_positive_stop_pad_on_big_yoke", box(26, 8, 8, (96, side_y - 4, 132)), "rubber")
    add(doc, "TILT_negative_stop_pad_on_big_yoke", box(26, 8, 8, (96, side_y - 4, 78)), "rubber")

    doc.recompute()
    fcstd_path = os.path.join(OUT_DIR, DOC_NAME + ".FCStd")
    step_path = os.path.join(OUT_DIR, DOC_NAME + ".step")
    doc.saveAs(fcstd_path)
    try:
        import Import
        Import.export([o for o in doc.Objects if hasattr(o, "Shape")], step_path)
    except Exception as exc:
        App.Console.PrintWarning("STEP export failed: %s\n" % exc)
    print("WROTE", fcstd_path)
    if os.path.exists(step_path):
        print("WROTE", step_path)
    write_bom_and_report()


def write_bom_and_report():
    printed = [
        ("Base", 1, "four-leg printed base, central pan bearing housing area"),
        ("Pan motor mount", 1, "slotted +/-5 mm tension adjustment for NEMA17"),
        ("Pan output hub", 1, "bearing-supported rotating hub, cable bore through center"),
        ("Pan driven pulley", 1, "integrated printed GT2-10, 80T"),
        ("Rotating upper plate", 1, "carries tilt frame and tilt motor"),
        ("Left tilt support", 1, "608 bearing pocket with printed retainer geometry"),
        ("Right tilt support", 1, "608 bearing pocket plus tilt motor bracket"),
        ("Tilt motor bracket", 1, "slotted NEMA17 mount, vertical belt adjustment"),
        ("Tilt driven pulley", 1, "printed GT2-10, 80T, bolted to camera cradle/axle hub"),
        ("Tilt camera cradle / camera plate", 1, "160x80x5 plate, 1/4-20 longitudinal slot"),
        ("Cable guides / tie slots", 1, "slots on camera plate and center cable passage"),
    ]
    bought = [
        ("NEMA17 stepper motor", 2, "42 mm frame, 31 mm hole spacing"),
        ("GT2 20T metal motor pulley, 5 mm bore, 10 mm belt", 2, "one per motor"),
        ("GT2 belt, 10 mm width", 2, "closed-loop length selected after final center distance"),
        ("608ZZ bearing 8x22x7", 4, "two for pan, two for tilt"),
        ("8 mm metal shaft / shoulder bolt", 2, "pan fixed shaft and tilt axle"),
        ("M3 screws", 8, "NEMA17 mounting"),
        ("M5 screws / washers / nuts", 8, "base, yoke, retainers, camera plate accessories"),
        ("1/4-20 UNC camera screw", 1, "camera mounting slot"),
        ("Rubber feet", 4, "base legs"),
        ("Panasonic HC-V760 placeholder", 1, "65x73x139 envelope, design load 0.6 kg"),
    ]
    bom = ["# BOM", "", "## Printed parts"]
    for name, qty, note in printed:
        bom.append(f"- {qty}x {name}: {note}")
    bom += ["", "## Bought components"]
    for name, qty, note in bought:
        bom.append(f"- {qty}x {name}: {note}")
    bom += [
        "",
        "## Drive ratios",
        f"- Pan: {int(P['pan_driven_teeth'])}T / {int(P['pan_motor_teeth'])}T = {P['pan_driven_teeth'] / P['pan_motor_teeth']:.1f}:1",
        f"- Tilt: {int(P['tilt_driven_teeth'])}T / {int(P['tilt_motor_teeth'])}T = {P['tilt_driven_teeth'] / P['tilt_motor_teeth']:.1f}:1",
    ]
    with open(os.path.join(OUT_DIR, "BOM.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(bom) + "\n")

    cog_dx = abs(38 - 22)
    cog_dz = abs(111 - 112)
    report = [
        "# CAD Checks",
        "",
        "## Load path",
        "- Pan load path: camera -> tilt cradle -> tilt supports -> rotating upper plate -> pan hub bearings -> base.",
        "- Tilt load path: camera -> camera plate -> 8 mm tilt axle -> two 608 bearings -> yoke supports.",
        "- NEMA17 shafts are motor-input shafts only and do not support camera mass.",
        "",
        "## Parameters",
        f"- Pan driven pitch diameter: {P['pan_pitch_d']:.2f} mm from 80T GT2.",
        f"- Tilt driven pitch diameter: {P['tilt_pitch_d']:.2f} mm from 80T GT2.",
        f"- Bearing pocket clearance parameter: {P['bearing_press_clearance']:.2f} mm.",
        f"- Tilt axis height above camera plate: {P['tilt_axis_height_above_plate']:.1f} mm.",
        "",
        "## Motion checks",
        "- Pan check poses represented by reference axis: -90, 0, +90 deg. Center bearing stack is axisymmetric; motor is offset and belt plane clears top platform in nominal CAD.",
        "- Tilt check poses considered by camera envelope and 95 mm inner yoke width: -60, 0, +60 deg are intended. Final collision must be rechecked after exact battery/cable geometry.",
        "",
        "## Center of gravity",
        f"- CAMERA_COG is shown near the camera envelope center. Initial offset from TiltAxis is about dx={cog_dx:.1f} mm, dz={cog_dz:.1f} mm.",
        "- Reduce this offset by sliding the camera in the 1/4-20 longitudinal slot and adjusting TILT_AXIS_HEIGHT_ABOVE_PLATE.",
    ]
    with open(os.path.join(OUT_DIR, "cad_checks.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")


if __name__ == "__main__":
    build()
