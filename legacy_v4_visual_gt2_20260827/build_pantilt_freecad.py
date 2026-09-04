import json
import math
import os

import FreeCAD as App
import Part


try:
    OUT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    OUT_DIR = os.getcwd()

DOC_NAME = "pantilt_hc_v760_reference_v4_inboard_tilt_pulley"

P = {
    "camera_w": 65.0,
    "camera_h": 73.0,
    "camera_d": 139.0,
    "camera_mass_kg": 0.6,
    "camera_plate_l": 160.0,
    "camera_plate_w": 78.0,
    "camera_plate_t": 5.0,
    "nema_w": 42.3,
    "nema_l": 48.0,
    "nema_bolt": 31.0,
    "nema_bolt_d": 3.5,
    "nema_pilot_d": 22.0,
    "tilt_trunnion_d": 7.9,
    "bearing_608_od": 22.0,
    "bearing_608_id": 8.0,
    "bearing_608_w": 7.0,
    "bearing_pocket_clearance": 0.12,
    "pan_bearing_od": 110.0,
    "pan_bearing_id": 86.0,
    "pan_bearing_h": 12.0,
    "pan_cable_bore": 55.0,
    "belt_pitch": 2.0,
    "belt_w": 10.0,
    "belt_t": 2.0,
    "pan_motor_teeth": 20,
    "pan_driven_teeth": 120,
    "tilt_motor_teeth": 20,
    "tilt_driven_teeth": 80,
    "pan_motor_x": -44.0,
    "pan_belt_z": 71.0,
    "tilt_axis_x": 0.0,
    "tilt_axis_z": 180.0,
    "tilt_motor_x": -46.0,
    "tilt_motor_z": 108.0,
    "tilt_belt_y": -45.8,
    "left_yoke_y": 51.0,
    "right_yoke_y": -61.5,
    "yoke_wall_t": 10.0,
    "tilt_motor_slide_y": -72.0,
}

P["pan_motor_pitch_d"] = P["pan_motor_teeth"] * P["belt_pitch"] / math.pi
P["pan_driven_pitch_d"] = P["pan_driven_teeth"] * P["belt_pitch"] / math.pi
P["tilt_motor_pitch_d"] = P["tilt_motor_teeth"] * P["belt_pitch"] / math.pi
P["tilt_driven_pitch_d"] = P["tilt_driven_teeth"] * P["belt_pitch"] / math.pi
P["right_bearing_y"] = P["right_yoke_y"] - 4.5
P["right_bearing_cap_y"] = P["right_bearing_y"] - 4.5


COLORS = {
    "printed": (0.66, 0.68, 0.70, 0.0),
    "printed_dark": (0.24, 0.27, 0.29, 0.0),
    "motor": (0.035, 0.04, 0.045, 0.0),
    "belt": (0.012, 0.014, 0.016, 0.0),
    "bearing": (0.43, 0.46, 0.49, 0.0),
    "steel": (0.64, 0.67, 0.70, 0.0),
    "pulley": (0.30, 0.33, 0.36, 0.0),
    "rubber": (0.04, 0.045, 0.05, 0.0),
    "camera": (0.055, 0.065, 0.075, 0.0),
    "camera_detail": (0.12, 0.14, 0.15, 0.0),
    "reference": (0.90, 0.08, 0.04, 0.0),
    "clearance": (0.10, 0.34, 0.86, 0.0),
}


def vec(x, y, z):
    return App.Vector(float(x), float(y), float(z))


def box(l, w, h, center):
    x, y, z = center
    return Part.makeBox(l, w, h, vec(x - l / 2, y - w / 2, z - h / 2))


def cyl_z(r, h, center):
    x, y, z = center
    return Part.makeCylinder(r, h, vec(x, y, z - h / 2), vec(0, 0, 1))


def cyl_y(r, h, center):
    x, y, z = center
    return Part.makeCylinder(r, h, vec(x, y - h / 2, z), vec(0, 1, 0))


def cyl_x(r, h, center):
    x, y, z = center
    return Part.makeCylinder(r, h, vec(x - h / 2, y, z), vec(1, 0, 0))


def ring_z(od, id_, h, center):
    return cyl_z(od / 2, h, center).cut(cyl_z(id_ / 2, h + 2, center))


def ring_y(od, id_, h, center):
    return cyl_y(od / 2, h, center).cut(cyl_y(id_ / 2, h + 2, center))


def slot_z(length, width, depth, center, along="x"):
    x, y, z = center
    if along == "x":
        core = box(max(0.1, length - width), width, depth, center)
        return core.fuse(cyl_z(width / 2, depth, (x - (length - width) / 2, y, z))).fuse(
            cyl_z(width / 2, depth, (x + (length - width) / 2, y, z))
        )
    core = box(width, max(0.1, length - width), depth, center)
    return core.fuse(cyl_z(width / 2, depth, (x, y - (length - width) / 2, z))).fuse(
        cyl_z(width / 2, depth, (x, y + (length - width) / 2, z))
    )


def slot_y(length, width, depth, center, along="z"):
    x, y, z = center
    if along == "z":
        core = box(width, depth, max(0.1, length - width), center)
        return core.fuse(cyl_y(width / 2, depth, (x, y, z - (length - width) / 2))).fuse(
            cyl_y(width / 2, depth, (x, y, z + (length - width) / 2))
        )
    core = box(max(0.1, length - width), depth, width, center)
    return core.fuse(cyl_y(width / 2, depth, (x - (length - width) / 2, y, z))).fuse(
        cyl_y(width / 2, depth, (x + (length - width) / 2, y, z))
    )


def prism_z(points, h, z0):
    vertices = [vec(x, y, z0) for x, y in points]
    wire = Part.makePolygon(vertices + [vertices[0]])
    return Part.Face(wire).extrude(vec(0, 0, h))


def prism_y(points, depth, y0):
    vertices = [vec(x, y0, z) for x, z in points]
    wire = Part.makePolygon(vertices + [vertices[0]])
    return Part.Face(wire).extrude(vec(0, depth, 0))


def rotate_z(shape, angle):
    out = shape.copy()
    out.rotate(vec(0, 0, 0), vec(0, 0, 1), angle)
    return out


def rotate_about_tilt(shape, angle):
    out = shape.copy()
    out.rotate(vec(P["tilt_axis_x"], 0, P["tilt_axis_z"]), vec(0, 1, 0), angle)
    return out


def oriented_run_xy(p1, p2, z, width, height):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    shape = Part.makeBox(length, width, height, vec(-length / 2, -width / 2, -height / 2))
    shape.Placement = App.Placement(
        vec((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, z),
        App.Rotation(vec(0, 0, 1), math.degrees(math.atan2(dy, dx))),
    )
    return shape


def oriented_run_xz(p1, p2, y, width, height):
    dx, dz = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dz)
    shape = Part.makeBox(length, width, height, vec(-length / 2, -width / 2, -height / 2))
    shape.Placement = App.Placement(
        vec((p1[0] + p2[0]) / 2, y, (p1[1] + p2[1]) / 2),
        App.Rotation(vec(0, 1, 0), -math.degrees(math.atan2(dz, dx))),
    )
    return shape


def external_tangent_points(a, ra, b, rb):
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy)
    ex, ey = dx / dist, dy / dist
    px, py = -ey, ex
    q = (ra - rb) / dist
    k = math.sqrt(max(0.0, 1.0 - q * q))
    pairs = []
    for side in (-1.0, 1.0):
        nx = q * ex + side * k * px
        ny = q * ey + side * k * py
        pairs.append(
            (
                (a[0] + ra * nx, a[1] + ra * ny),
                (b[0] + rb * nx, b[1] + rb * ny),
            )
        )
    return pairs


def belt_z(a, da, b, db, z):
    ra, rb = da / 2, db / 2
    parts = [
        ring_z(da + P["belt_t"], da - P["belt_t"], P["belt_w"], (a[0], a[1], z)),
        ring_z(db + P["belt_t"], db - P["belt_t"], P["belt_w"], (b[0], b[1], z)),
    ]
    for p1, p2 in external_tangent_points(a, ra, b, rb):
        parts.append(oriented_run_xy(p1, p2, z, P["belt_t"], P["belt_w"]))
    return Part.makeCompound(parts)


def belt_y(a, da, b, db, y):
    ra, rb = da / 2, db / 2
    parts = [
        ring_y(da + P["belt_t"], da - P["belt_t"], P["belt_w"], (a[0], y, a[1])),
        ring_y(db + P["belt_t"], db - P["belt_t"], P["belt_w"], (b[0], y, b[1])),
    ]
    for p1, p2 in external_tangent_points(a, ra, b, rb):
        parts.append(oriented_run_xz(p1, p2, y, P["belt_w"], P["belt_t"]))
    return Part.makeCompound(parts)


def teeth_z(pitch_d, h, z, teeth, tooth_h=1.8):
    tangential = max(0.8, math.pi * pitch_d / teeth * 0.44)
    radius = pitch_d / 2 + tooth_h / 2
    parts = []
    for index in range(teeth):
        tooth = box(tooth_h, tangential, h, (radius, 0, z))
        tooth.rotate(vec(0, 0, 0), vec(0, 0, 1), 360.0 * index / teeth)
        parts.append(tooth)
    return Part.makeCompound(parts)


def teeth_y(pitch_d, width, center, teeth, tooth_h=1.8):
    x0, y0, z0 = center
    tangential = max(0.8, math.pi * pitch_d / teeth * 0.44)
    radius = pitch_d / 2 + tooth_h / 2
    parts = []
    for index in range(teeth):
        tooth = box(tooth_h, width, tangential, (radius, 0, 0))
        tooth.Placement = App.Placement(
            vec(x0, y0, z0),
            App.Rotation(vec(0, 1, 0), -360.0 * index / teeth),
        )
        parts.append(tooth)
    return Part.makeCompound(parts)


def pulley_z(pitch_d, bore, width, center, teeth=None):
    x, y, z = center
    body = ring_z(pitch_d + 1.2, bore, width, center)
    flanges = ring_z(pitch_d + 5.0, bore, 1.2, (x, y, z - width / 2 - 0.6)).fuse(
        ring_z(pitch_d + 5.0, bore, 1.2, (x, y, z + width / 2 + 0.6))
    )
    tooth_shape = teeth_z(pitch_d, width, z, teeth) if teeth else Part.Shape()
    return body, flanges, tooth_shape


def pulley_y(pitch_d, bore, width, center, teeth=None):
    x, y, z = center
    body = ring_y(pitch_d + 1.2, bore, width, center)
    flanges = ring_y(pitch_d + 5.0, bore, 1.2, (x, y - width / 2 - 0.6, z)).fuse(
        ring_y(pitch_d + 5.0, bore, 1.2, (x, y + width / 2 + 0.6, z))
    )
    tooth_shape = teeth_y(pitch_d, width, center, teeth) if teeth else Part.Shape()
    return body, flanges, tooth_shape


def solid_integral_pulley_y(pitch_d, width, center, teeth):
    x, y, z = center
    shape = cyl_y((pitch_d + 1.2) / 2, width, center)
    shape = shape.fuse(
        cyl_y((pitch_d + 5.0) / 2, 1.2, (x, y - width / 2 - 0.5, z))
    )
    shape = shape.fuse(
        cyl_y((pitch_d + 5.0) / 2, 1.2, (x, y + width / 2 + 0.5, z))
    )
    for tooth in teeth_y(pitch_d, width, center, teeth).Solids:
        shape = shape.fuse(tooth)
    return shape.removeSplitter()


def add(doc, group, label, shape, material, transparency=0):
    obj = doc.addObject("Part::Feature", label)
    obj.Label = label
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "MaterialRole", "Design")
    obj.MaterialRole = material
    group.addObject(obj)
    try:
        obj.ViewObject.ShapeColor = COLORS[material]
        obj.ViewObject.LineColor = COLORS[material]
        obj.ViewObject.Transparency = transparency
        obj.ViewObject.DisplayMode = "Shaded"
    except Exception:
        pass
    return obj


def make_spreadsheet(doc):
    sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
    values = [
        ("CAMERA_WIDTH", P["camera_w"], "mm"),
        ("CAMERA_HEIGHT", P["camera_h"], "mm"),
        ("CAMERA_LENGTH", P["camera_d"], "mm"),
        ("CAMERA_MASS", P["camera_mass_kg"], "kg"),
        ("PAN_BEARING_OD", P["pan_bearing_od"], "mm"),
        ("PAN_BEARING_ID", P["pan_bearing_id"], "mm"),
        ("PAN_CABLE_BORE", P["pan_cable_bore"], "mm"),
        ("PAN_MOTOR_TEETH", P["pan_motor_teeth"], "teeth"),
        ("PAN_DRIVEN_TEETH", P["pan_driven_teeth"], "teeth"),
        ("PAN_RATIO", P["pan_driven_teeth"] / P["pan_motor_teeth"], "ratio"),
        ("TILT_BEARING_OD", P["bearing_608_od"], "mm"),
        ("TILT_TRUNNION_D", P["tilt_trunnion_d"], "mm"),
        ("TILT_MOTOR_TEETH", P["tilt_motor_teeth"], "teeth"),
        ("TILT_DRIVEN_TEETH", P["tilt_driven_teeth"], "teeth"),
        ("TILT_RATIO", P["tilt_driven_teeth"] / P["tilt_motor_teeth"], "ratio"),
        ("TILT_AXIS_Z", P["tilt_axis_z"], "mm"),
        ("TILT_BELT_PLANE_Y", P["tilt_belt_y"], "mm"),
        ("RIGHT_YOKE_CENTER_Y", P["right_yoke_y"], "mm"),
        ("RIGHT_TILT_BEARING_Y", P["right_bearing_y"], "mm"),
    ]
    sheet.set("A1", "PARAMETER")
    sheet.set("B1", "VALUE")
    sheet.set("C1", "UNIT")
    for row, (name, value, unit) in enumerate(values, start=2):
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", str(round(float(value), 4)))
        sheet.set(f"C{row}", unit)
        try:
            sheet.setAlias(f"B{row}", name)
        except Exception:
            pass


def build_base(doc, base_group, objects):
    base = cyl_z(62, 10, (0, 0, 5))
    leg_points = [(35, -24), (120, -19), (140, -12), (140, 12), (120, 19), (35, 24)]
    window_a = [(63, -13), (89, -10), (63, -3)]
    window_b = [(63, 3), (89, 10), (63, 13)]
    for angle in (0, 120, 240):
        leg = prism_z(leg_points, 10, 0)
        leg = leg.cut(prism_z(window_a, 12, -1)).cut(prism_z(window_b, 12, -1))
        leg = leg.cut(cyl_z(3.6, 12, (128, 0, 5)))
        base = base.fuse(rotate_z(leg, angle))
        foot = rotate_z(cyl_z(9, 4, (128, 0, -2)), angle)
        objects[f"BASE_rubber_foot_{angle}"] = add(
            doc, base_group, f"BASE_rubber_foot_{angle}", foot, "rubber"
        )
    objects["BASE_three_leg_frame"] = add(doc, base_group, "BASE_three_leg_frame", base, "printed")

    tower = ring_z(116, 94, 46, (0, 0, 33))
    tower = tower.cut(box(56, 58, 50, (P["pan_motor_x"], 0, 33)))
    objects["BASE_pan_tower_shell"] = add(
        doc, base_group, "BASE_pan_tower_shell", tower, "printed"
    )

    mount = box(74, 58, 5, (P["pan_motor_x"], 0, 12.5))
    for sx in (-1, 1):
        for sy in (-1, 1):
            mount = mount.cut(
                slot_z(
                    14,
                    P["nema_bolt_d"],
                    7,
                    (
                        P["pan_motor_x"] + sx * P["nema_bolt"] / 2,
                        sy * P["nema_bolt"] / 2,
                        12.5,
                    ),
                    along="x",
                )
            )
    objects["BASE_pan_motor_radial_slide"] = add(
        doc, base_group, "BASE_pan_motor_radial_slide", mount, "printed_dark"
    )

    objects["BASE_pan_motor_NEMA17"] = add(
        doc,
        base_group,
        "BASE_pan_motor_NEMA17",
        box(P["nema_w"], P["nema_w"], P["nema_l"], (P["pan_motor_x"], 0, 38)),
        "motor",
    )
    objects["BASE_pan_motor_pilot"] = add(
        doc,
        base_group,
        "BASE_pan_motor_pilot",
        cyl_z(P["nema_pilot_d"] / 2, 2, (P["pan_motor_x"], 0, 63)),
        "steel",
    )
    objects["BASE_pan_motor_shaft"] = add(
        doc,
        base_group,
        "BASE_pan_motor_shaft",
        cyl_z(2.5, 22, (P["pan_motor_x"], 0, 73)),
        "steel",
    )
    motor_body, motor_flanges, _ = pulley_z(
        P["pan_motor_pitch_d"], 5, P["belt_w"], (P["pan_motor_x"], 0, P["pan_belt_z"])
    )
    objects["BASE_pan_motor_20T_pulley"] = add(
        doc, base_group, "BASE_pan_motor_20T_pulley", motor_body, "pulley"
    )
    objects["BASE_pan_motor_20T_flanges"] = add(
        doc, base_group, "BASE_pan_motor_20T_flanges", motor_flanges, "pulley"
    )

    objects["BASE_pan_turntable_lower_race"] = add(
        doc,
        base_group,
        "BASE_pan_turntable_lower_race",
        ring_z(P["pan_bearing_od"], P["pan_bearing_id"], 3, (0, 0, 57.5)),
        "bearing",
    )
    objects["BASE_pan_turntable_sealed_cartridge"] = add(
        doc,
        base_group,
        "BASE_pan_turntable_sealed_cartridge",
        ring_z(108, 88, 5, (0, 0, 61.5)),
        "bearing",
    )


def yoke_side_shape(side):
    yc = P["left_yoke_y"] if side > 0 else P["right_yoke_y"]
    wall_t = P["yoke_wall_t"]
    y0 = yc - wall_t / 2
    points = [
        (-76, 83),
        (52, 83),
        (52, 97),
        (31, 97),
        (28, 202),
        (-28, 202),
        (-31, 140),
        (-76, 140),
    ]
    plate = prism_y(points, wall_t, y0)
    plate = plate.fuse(cyl_y(19, 16, (P["tilt_axis_x"], yc, P["tilt_axis_z"])))

    outer = yc + side * 4.5
    plate = plate.cut(
        cyl_y(
            (P["bearing_608_od"] + P["bearing_pocket_clearance"]) / 2,
            9,
            (P["tilt_axis_x"], outer, P["tilt_axis_z"]),
        )
    )
    plate = plate.cut(
        cyl_y(
            P["bearing_608_id"] / 2 + 0.25,
            20,
            (P["tilt_axis_x"], yc, P["tilt_axis_z"]),
        )
    )
    if side > 0:
        plate = plate.cut(slot_y(34, 14, 12, (-52, yc, 117), along="z"))
    else:
        plate = plate.cut(
            cyl_y(3.2, 30, (P["tilt_motor_x"], yc, P["tilt_motor_z"]))
        )
    return plate


def build_pan_rotating(doc, pan_group, objects):
    objects["PAN_ROTATING_turntable_upper_race"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_turntable_upper_race",
        ring_z(P["pan_bearing_od"], P["pan_bearing_id"], 3, (0, 0, 65.5)),
        "bearing",
    )
    objects["PAN_ROTATING_bearing_adapter"] = add(
        doc, pan_group, "PAN_ROTATING_bearing_adapter", ring_z(116, 84, 10, (0, 0, 72)), "printed_dark"
    )

    drive_body, drive_flanges, drive_teeth = pulley_z(
        P["pan_driven_pitch_d"],
        P["pan_cable_bore"],
        P["belt_w"],
        (0, 0, P["pan_belt_z"]),
        teeth=P["pan_driven_teeth"],
    )
    objects["PAN_ROTATING_120T_drive_ring"] = add(
        doc, pan_group, "PAN_ROTATING_120T_drive_ring", drive_body, "pulley"
    )
    objects["PAN_ROTATING_120T_drive_flanges"] = add(
        doc, pan_group, "PAN_ROTATING_120T_drive_flanges", drive_flanges, "pulley"
    )
    objects["PAN_ROTATING_120T_exact_tooth_count"] = add(
        doc, pan_group, "PAN_ROTATING_120T_exact_tooth_count", drive_teeth, "pulley"
    )

    objects["BASE_pan_GT2_252mm_belt"] = add(
        doc,
        pan_group,
        "BASE_pan_GT2_252mm_belt",
        belt_z(
            (P["pan_motor_x"], 0),
            P["pan_motor_pitch_d"],
            (0, 0),
            P["pan_driven_pitch_d"],
            P["pan_belt_z"],
        ),
        "belt",
    )

    objects["PAN_ROTATING_platform_with_cable_bore"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_platform_with_cable_bore",
        ring_z(118, P["pan_cable_bore"], 6, (0, 0, 80)),
        "printed",
    )
    objects["PAN_ROTATING_cable_guide"] = add(
        doc, pan_group, "PAN_ROTATING_cable_guide", ring_z(64, 55, 12, (0, 0, 84)), "printed_dark"
    )

    objects["PAN_ROTATING_left_yoke"] = add(
        doc, pan_group, "PAN_ROTATING_left_yoke", yoke_side_shape(1), "printed"
    )
    objects["PAN_ROTATING_right_yoke_motor_mount"] = add(
        doc, pan_group, "PAN_ROTATING_right_yoke_motor_mount", yoke_side_shape(-1), "printed"
    )
    for side in (-1, 1):
        yc = P["left_yoke_y"] if side > 0 else P["right_yoke_y"]
        gusset_y0 = yc - 8 if side > 0 else yc
        gusset = prism_y([(-70, 83), (-20, 83), (-20, 112)], 8, gusset_y0)
        objects[f"PAN_ROTATING_yoke_gusset_{side}"] = add(
            doc, pan_group, f"PAN_ROTATING_yoke_gusset_{side}", gusset, "printed_dark"
        )

    objects["PAN_ROTATING_left_608_bearing"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_left_608_bearing",
        ring_y(P["bearing_608_od"], P["bearing_608_id"], P["bearing_608_w"], (0, 55.5, P["tilt_axis_z"])),
        "bearing",
    )
    objects["PAN_ROTATING_right_608_bearing"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_right_608_bearing",
        ring_y(
            P["bearing_608_od"],
            P["bearing_608_id"],
            P["bearing_608_w"],
            (0, P["right_bearing_y"], P["tilt_axis_z"]),
        ),
        "bearing",
    )
    objects["PAN_ROTATING_left_bearing_cap"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_left_bearing_cap",
        ring_y(32, 8.6, 2, (0, 60, P["tilt_axis_z"])),
        "printed_dark",
    )
    objects["PAN_ROTATING_right_bearing_cap"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_right_bearing_cap",
        ring_y(32, 8.6, 2, (0, P["right_bearing_cap_y"], P["tilt_axis_z"])),
        "printed_dark",
    )

    motor_slide = box(
        70,
        3,
        70,
        (P["tilt_motor_x"], P["tilt_motor_slide_y"], P["tilt_motor_z"]),
    )
    motor_slide = motor_slide.cut(
        slot_y(
            35,
            P["nema_pilot_d"] + 1,
            5,
            (P["tilt_motor_x"], P["tilt_motor_slide_y"], P["tilt_motor_z"]),
            along="z",
        )
    )
    for sx in (-1, 1):
        for sz in (-1, 1):
            motor_slide = motor_slide.cut(
                slot_y(
                    17,
                    P["nema_bolt_d"],
                    5,
                    (
                        P["tilt_motor_x"] + sx * P["nema_bolt"] / 2,
                        P["tilt_motor_slide_y"],
                        P["tilt_motor_z"] + sz * P["nema_bolt"] / 2,
                    ),
                    along="z",
                )
            )
    objects["PAN_ROTATING_tilt_motor_vertical_slide"] = add(
        doc, pan_group, "PAN_ROTATING_tilt_motor_vertical_slide", motor_slide, "printed_dark"
    )
    right_yoke_outer_y = P["right_yoke_y"] - P["yoke_wall_t"] / 2
    slide_inner_y = P["tilt_motor_slide_y"] + 1.5
    standoff_length = right_yoke_outer_y - slide_inner_y
    standoff_center_y = (right_yoke_outer_y + slide_inner_y) / 2
    standoffs = Part.makeCompound(
        [
            cyl_y(
                4.5,
                standoff_length,
                (P["tilt_motor_x"] + sx * 28, standoff_center_y, P["tilt_motor_z"] + sz * 28),
            )
            for sx in (-1, 1)
            for sz in (-1, 1)
        ]
    )
    objects["PAN_ROTATING_tilt_motor_mount_standoffs"] = add(
        doc, pan_group, "PAN_ROTATING_tilt_motor_mount_standoffs", standoffs, "printed"
    )

    objects["PAN_ROTATING_tilt_motor_NEMA17"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_tilt_motor_NEMA17",
        box(
            P["nema_w"],
            P["nema_l"],
            P["nema_w"],
            (P["tilt_motor_x"], P["tilt_motor_slide_y"] - 25.5, P["tilt_motor_z"]),
        ),
        "motor",
    )
    objects["PAN_ROTATING_tilt_motor_pilot"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_tilt_motor_pilot",
        cyl_y(
            P["nema_pilot_d"] / 2,
            2,
            (P["tilt_motor_x"], P["tilt_motor_slide_y"] + 0.5, P["tilt_motor_z"]),
        ),
        "steel",
    )
    objects["PAN_ROTATING_tilt_motor_shaft"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_tilt_motor_shaft",
        cyl_y(2.5, 34, (P["tilt_motor_x"], -56.5, P["tilt_motor_z"])),
        "steel",
    )

    motor_pulley, motor_flanges, _ = pulley_y(
        P["tilt_motor_pitch_d"],
        5,
        P["belt_w"],
        (P["tilt_motor_x"], P["tilt_belt_y"], P["tilt_motor_z"]),
    )
    objects["PAN_ROTATING_tilt_motor_20T_pulley"] = add(
        doc, pan_group, "PAN_ROTATING_tilt_motor_20T_pulley", motor_pulley, "pulley"
    )
    objects["PAN_ROTATING_tilt_motor_20T_flanges"] = add(
        doc, pan_group, "PAN_ROTATING_tilt_motor_20T_flanges", motor_flanges, "pulley"
    )

    objects["PAN_ROTATING_tilt_GT2_280mm_belt"] = add(
        doc,
        pan_group,
        "PAN_ROTATING_tilt_GT2_280mm_belt",
        belt_y(
            (P["tilt_motor_x"], P["tilt_motor_z"]),
            P["tilt_motor_pitch_d"],
            (P["tilt_axis_x"], P["tilt_axis_z"]),
            P["tilt_driven_pitch_d"],
            P["tilt_belt_y"],
        ),
        "belt",
    )


def build_tilt_rotating(doc, tilt_group, objects):
    plate_z = 140.0
    plate = box(P["camera_plate_l"], P["camera_plate_w"], P["camera_plate_t"], (0, 0, plate_z))
    plate = plate.cut(slot_z(58, 7.0, 7, (0, 0, plate_z), along="x"))
    for x in (-48, 48):
        plate = plate.cut(slot_z(22, 5, 7, (x, 28, plate_z), along="x"))
        plate = plate.cut(slot_z(22, 5, 7, (x, -28, plate_z), along="x"))
    one_piece = plate
    for side in (-1, 1):
        one_piece = one_piece.fuse(box(132, 6, 44, (0, side * 37, 161)))
        one_piece = one_piece.fuse(cyl_y(13, 8, (0, side * 37, P["tilt_axis_z"])))

    left_trunnion = cyl_y(
        P["tilt_trunnion_d"] / 2,
        25,
        (P["tilt_axis_x"], 51.5, P["tilt_axis_z"]),
    )
    right_trunnion = cyl_y(
        P["tilt_trunnion_d"] / 2,
        22.5,
        (P["tilt_axis_x"], -61.25, P["tilt_axis_z"]),
    )
    integral_pulley = solid_integral_pulley_y(
        P["tilt_driven_pitch_d"],
        P["belt_w"],
        (P["tilt_axis_x"], P["tilt_belt_y"], P["tilt_axis_z"]),
        P["tilt_driven_teeth"],
    )
    for connected_shape in (left_trunnion, right_trunnion, integral_pulley):
        one_piece = one_piece.fuse(connected_shape)
    one_piece = one_piece.removeSplitter()
    objects["TILT_ROTATING_one_piece_cradle_trunnions_80T"] = add(
        doc,
        tilt_group,
        "TILT_ROTATING_one_piece_cradle_trunnions_80T",
        one_piece,
        "printed",
    )

    camera_center_z = plate_z + P["camera_plate_t"] / 2 + P["camera_h"] / 2
    objects["CAMERA_HC_V760_body_placeholder"] = add(
        doc,
        tilt_group,
        "CAMERA_HC_V760_body_placeholder",
        box(P["camera_d"], P["camera_w"], P["camera_h"], (0, 0, camera_center_z)),
        "camera",
        transparency=12,
    )
    objects["CAMERA_HC_V760_lens"] = add(
        doc,
        tilt_group,
        "CAMERA_HC_V760_lens",
        cyl_x(18, 20, (P["camera_d"] / 2 + 10, 0, camera_center_z + 2)),
        "camera_detail",
    )
    objects["CAMERA_HC_V760_rear_battery"] = add(
        doc,
        tilt_group,
        "CAMERA_HC_V760_rear_battery",
        box(18, 48, 52, (-P["camera_d"] / 2 - 7, 0, camera_center_z)),
        "camera_detail",
    )
    objects["CAMERA_flip_screen_clearance_closed"] = add(
        doc,
        tilt_group,
        "CAMERA_flip_screen_clearance_closed",
        box(68, 3, 45, (-5, P["camera_w"] / 2 + 9, camera_center_z)),
        "clearance",
        transparency=72,
    )
    objects["CAMERA_nominal_COG"] = add(
        doc,
        tilt_group,
        "CAMERA_nominal_COG",
        Part.makeSphere(3.2, vec(0, 0, camera_center_z)),
        "reference",
    )
    objects["CAMERA_optical_axis"] = add(
        doc,
        tilt_group,
        "CAMERA_optical_axis",
        cyl_x(0.9, 210, (12, 0, camera_center_z + 2)),
        "reference",
    )
    objects["TILT_ROTATING_camera_mount_screw"] = add(
        doc,
        tilt_group,
        "TILT_ROTATING_camera_mount_screw",
        cyl_z(3.1, 10, (0, 0, 142)),
        "steel",
    )


def add_references(doc, reference_group, objects):
    objects["REFERENCE_pan_axis"] = add(
        doc,
        reference_group,
        "REFERENCE_pan_axis",
        cyl_z(1.0, 235, (0, 0, 117.5)),
        "reference",
    )
    objects["REFERENCE_tilt_axis"] = add(
        doc,
        reference_group,
        "REFERENCE_tilt_axis",
        cyl_y(1.0, 170, (P["tilt_axis_x"], 0, P["tilt_axis_z"])),
        "reference",
    )


def common_volume(a, b):
    return a.common(b).Volume


def validate_geometry(doc, objects):
    pair_names = [
        ("tilt_right_yoke_vs_motor_pulley", "PAN_ROTATING_right_yoke_motor_mount", "PAN_ROTATING_tilt_motor_20T_pulley"),
        ("tilt_right_yoke_vs_motor_shaft", "PAN_ROTATING_right_yoke_motor_mount", "PAN_ROTATING_tilt_motor_shaft"),
        ("tilt_right_yoke_vs_integral_cradle", "PAN_ROTATING_right_yoke_motor_mount", "TILT_ROTATING_one_piece_cradle_trunnions_80T"),
        ("tilt_right_608_vs_integral_cradle", "PAN_ROTATING_right_608_bearing", "TILT_ROTATING_one_piece_cradle_trunnions_80T"),
        ("tilt_left_608_vs_integral_cradle", "PAN_ROTATING_left_608_bearing", "TILT_ROTATING_one_piece_cradle_trunnions_80T"),
        ("tilt_right_yoke_vs_belt", "PAN_ROTATING_right_yoke_motor_mount", "PAN_ROTATING_tilt_GT2_280mm_belt"),
        ("tilt_standoffs_vs_belt", "PAN_ROTATING_tilt_motor_mount_standoffs", "PAN_ROTATING_tilt_GT2_280mm_belt"),
        ("tilt_slide_vs_belt", "PAN_ROTATING_tilt_motor_vertical_slide", "PAN_ROTATING_tilt_GT2_280mm_belt"),
        ("pan_tower_vs_motor", "BASE_pan_tower_shell", "BASE_pan_motor_NEMA17"),
        ("pan_adapter_vs_belt", "PAN_ROTATING_bearing_adapter", "BASE_pan_GT2_252mm_belt"),
        ("camera_vs_tilt_motor_nominal", "CAMERA_HC_V760_body_placeholder", "PAN_ROTATING_tilt_motor_NEMA17"),
        ("integral_cradle_vs_tilt_motor_nominal", "TILT_ROTATING_one_piece_cradle_trunnions_80T", "PAN_ROTATING_tilt_motor_NEMA17"),
    ]
    pair_results = {}
    for name, a, b in pair_names:
        pair_results[name] = round(common_volume(objects[a].Shape, objects[b].Shape), 6)

    moving_labels = [
        "TILT_ROTATING_one_piece_cradle_trunnions_80T",
        "CAMERA_HC_V760_body_placeholder",
        "CAMERA_HC_V760_lens",
        "CAMERA_HC_V760_rear_battery",
    ]
    obstacle_labels = [
        "PAN_ROTATING_platform_with_cable_bore",
        "PAN_ROTATING_left_yoke",
        "PAN_ROTATING_right_yoke_motor_mount",
        "PAN_ROTATING_tilt_motor_NEMA17",
    ]
    pose_results = {}
    pose_pair_results = {}
    for angle in (-60, 0, 60):
        total = 0.0
        details = {}
        for moving_label in moving_labels:
            moving_shape = rotate_about_tilt(objects[moving_label].Shape, angle)
            for obstacle_label in obstacle_labels:
                volume = common_volume(moving_shape, objects[obstacle_label].Shape)
                total += volume
                if volume > 0.000001:
                    details[f"{moving_label} vs {obstacle_label}"] = round(volume, 6)
        pose_results[str(angle)] = round(total, 6)
        pose_pair_results[str(angle)] = details

    invalid = [
        obj.Label
        for obj in doc.Objects
        if hasattr(obj, "Shape") and not obj.Shape.isNull() and not obj.Shape.isValid()
    ]
    integral_label = "TILT_ROTATING_one_piece_cradle_trunnions_80T"
    integral_feature_count = sum(obj.Label == integral_label for obj in doc.Objects)
    integral_solid_count = len(objects[integral_label].Shape.Solids)
    through_tilt_shaft_present = any(
        "TILT_ROTATING_8mm_steel_axle" in obj.Label or "continuous_tilt_axle" in obj.Label
        for obj in doc.Objects
    )
    central_axis_probe = cyl_y(
        P["tilt_trunnion_d"] / 2,
        60,
        (P["tilt_axis_x"], 0, P["tilt_axis_z"]),
    )
    center_cross_shaft_material = round(
        common_volume(objects[integral_label].Shape, central_axis_probe), 6
    )
    pulley_half_envelope = P["belt_w"] / 2 + 1.1
    pulley_order_margin = round(
        abs(P["right_bearing_y"]) - abs(P["tilt_belt_y"]), 6
    )
    pulley_outboard_edge = P["tilt_belt_y"] - pulley_half_envelope
    right_yoke_boss_inboard_edge = P["right_yoke_y"] + 8.0
    pulley_to_right_yoke_clearance = round(
        pulley_outboard_edge - right_yoke_boss_inboard_edge, 6
    )
    pulley_inboard_edge = P["tilt_belt_y"] + pulley_half_envelope
    camera_negative_y_edge = -P["camera_w"] / 2
    pulley_to_camera_clearance = round(
        camera_negative_y_edge - pulley_inboard_edge, 6
    )
    pulley_closer_to_camera_than_right_bearing = pulley_order_margin > 0
    all_volumes = list(pair_results.values()) + list(pose_results.values())
    result = {
        "schema_version": 3,
        "design": DOC_NAME,
        "valid_breps": len(invalid) == 0,
        "invalid_objects": invalid,
        "interference_tolerance_mm3": 0.01,
        "pair_interference_mm3": pair_results,
        "tilt_pose_interference_mm3": pose_results,
        "tilt_pose_pair_interference_mm3": pose_pair_results,
        "integral_tilt_part_features": integral_feature_count,
        "integral_tilt_solid_count": integral_solid_count,
        "through_tilt_shaft_present": through_tilt_shaft_present,
        "center_cross_shaft_material_mm3": center_cross_shaft_material,
        "pulley_closer_to_camera_than_right_bearing": pulley_closer_to_camera_than_right_bearing,
        "pulley_to_right_bearing_center_margin_mm": pulley_order_margin,
        "pulley_to_right_yoke_clearance_mm": pulley_to_right_yoke_clearance,
        "pulley_to_camera_clearance_mm": pulley_to_camera_clearance,
        "passed": (
            len(invalid) == 0
            and all(value <= 0.01 for value in all_volumes)
            and integral_feature_count == 1
            and integral_solid_count == 1
            and not through_tilt_shaft_present
            and center_cross_shaft_material <= 0.01
            and pulley_closer_to_camera_than_right_bearing
            and pulley_order_margin >= 15.0
            and pulley_to_right_yoke_clearance >= 1.0
            and pulley_to_camera_clearance >= 5.0
        ),
    }
    with open(os.path.join(OUT_DIR, "geometry_validation.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return result


def write_docs(validation):
    pan_ratio = P["pan_driven_teeth"] / P["pan_motor_teeth"]
    tilt_ratio = P["tilt_driven_teeth"] / P["tilt_motor_teeth"]
    camera_cog_z = 140 + P["camera_plate_t"] / 2 + P["camera_h"] / 2
    cog_offset = abs(P["tilt_axis_z"] - camera_cog_z)
    static_torque = P["camera_mass_kg"] * 9.81 * cog_offset / 1000

    bom = f"""# BOM V4

## Printed concept parts
- 1x three-leg base with motor bay and gusseted feet
- 1x pan motor radial slide plate
- 1x pan bearing adapter and 120T driven ring
- 1x rotating pan platform with {P['pan_cable_bore']:.0f} mm cable bore
- 1x compact two-sided yoke with integrated tilt motor mount
- 2x 608 bearing caps
- 1x one-piece printed tilt cradle with camera plate, both cheeks, two 7.9 mm trunnions, and integral inboard 80T pulley

## Bought components
- 2x NEMA17 stepper motor, 42 mm frame
- 1x long-shaft tilt NEMA17 or 5 mm shaft extension rated for the 20T pulley
- 1x 110x86x12 mm precision turntable bearing
- 2x 608-2RS bearing, 8x22x7 mm
- 1x GT2 20T metal pulley and 1x 120T driven pulley for pan
- 1x GT2 20T metal pulley for tilt; the 80T driven pulley is integral to the printed cradle
- 1x GT2 10 mm belt, nominal 252 mm for pan
- 1x GT2 10 mm belt, nominal 280 mm for tilt
- 1x 1/4-20 camera screw
- M3 motor screws, M4 bearing-cap screws, M5 base fasteners
- 3x rubber feet

## Ratios
- Pan: {P['pan_driven_teeth']}T / {P['pan_motor_teeth']}T = {pan_ratio:.1f}:1
- Tilt: {P['tilt_driven_teeth']}T / {P['tilt_motor_teeth']}T = {tilt_ratio:.1f}:1
"""
    with open(os.path.join(OUT_DIR, "BOM.md"), "w", encoding="utf-8") as handle:
        handle.write(bom)

    pair_lines = "\n".join(
        f"- {name}: {volume:.6f} mm3"
        for name, volume in validation["pair_interference_mm3"].items()
    )
    pose_lines = "\n".join(
        f"- Tilt {angle} deg: {volume:.6f} mm3"
        for angle, volume in validation["tilt_pose_interference_mm3"].items()
    )
    report = f"""# CAD Checks V4

## Architecture
- Three-leg reference-like base with the pan motor below the turntable.
- Pan load path uses a 110x86x12 mm turntable bearing.
- Tilt rotating structure is one printed solid: plate, cheeks, hubs, two short {P['tilt_trunnion_d']:.1f} mm trunnions, and integral 80T pulley.
- Right-side order from camera outward is 80T pulley, plastic bearing trunnion, and 608 bearing.
- There is no shaft or printed material crossing the camera volume along the central tilt-axis span.
- Two shoulder-seated 608 bearings remain fixed in the pan yoke.
- Tilt belt plane is inboard of the right yoke wall at Y={P['tilt_belt_y']:.1f} mm.
- Central pan cable passage is {P['pan_cable_bore']:.1f} mm.

## Drive
- Pan pitch diameter: {P['pan_driven_pitch_d']:.2f} mm, ratio {pan_ratio:.1f}:1.
- Tilt pitch diameter: {P['tilt_driven_pitch_d']:.2f} mm, ratio {tilt_ratio:.1f}:1.
- Visual pulley geometry contains exactly {P['pan_driven_teeth']} pan teeth and {P['tilt_driven_teeth']} tilt teeth.
- Motor slots follow each belt tension direction.

## Balance
- Nominal camera COG offset from the tilt axis: {cog_offset:.2f} mm.
- Nominal camera-only gravity torque: {static_torque:.4f} N m.

## Interference checks
{pair_lines}

## Tilt pose checks
{pose_lines}

## Result
- Valid B-reps: {validation['valid_breps']}
- Integral tilt Part::Feature count: {validation['integral_tilt_part_features']}
- Integral tilt solid count: {validation['integral_tilt_solid_count']}
- Through tilt shaft present: {validation['through_tilt_shaft_present']}
- Central cross-shaft material: {validation['center_cross_shaft_material_mm3']:.6f} mm3
- Pulley closer to camera than right bearing: {validation['pulley_closer_to_camera_than_right_bearing']}
- Pulley-to-bearing center margin: {validation['pulley_to_right_bearing_center_margin_mm']:.2f} mm
- Pulley-to-right-yoke clearance: {validation['pulley_to_right_yoke_clearance_mm']:.2f} mm
- Pulley-to-camera clearance: {validation['pulley_to_camera_clearance_mm']:.2f} mm
- Geometry validation passed: {validation['passed']}

## Production limitations
- Replace visual pulley teeth with an exact vendor GT2 profile.
- Prototype the printed trunnion fit and check wear, creep, and layer orientation at both 608 bearings.
- Select a supported long-shaft tilt motor or shaft extension and verify runout at the inboard 20T pulley.
- Confirm the selected turntable bearing and closed-loop belt dimensions.
- Measure the physical HC-V760 including battery, LCD travel, lens, and connectors.
- Add final screw threads, inserts, tolerances, fillets, and print-orientation details.
"""
    with open(os.path.join(OUT_DIR, "cad_checks.md"), "w", encoding="utf-8") as handle:
        handle.write(report)


def build():
    try:
        old = App.getDocument(DOC_NAME)
        App.closeDocument(old.Name)
    except Exception:
        pass
    doc = App.newDocument(DOC_NAME)
    make_spreadsheet(doc)

    assembly = doc.addObject("App::Part", "Assembly")
    assembly.Label = "PAN_TILT_REFERENCE_V4_INBOARD_TILT_PULLEY"
    base_group = doc.addObject("App::Part", "BaseFixed")
    pan_group = doc.addObject("App::Part", "PanRotating")
    tilt_group = doc.addObject("App::Part", "TiltRotating")
    reference_group = doc.addObject("App::Part", "References")
    assembly.addObject(base_group)
    assembly.addObject(pan_group)
    pan_group.addObject(tilt_group)
    assembly.addObject(reference_group)

    pan_group.addProperty("App::PropertyAngle", "PanAngle", "Kinematics")
    tilt_group.addProperty("App::PropertyAngle", "TiltAngle", "Kinematics")
    pan_group.PanAngle = 0
    tilt_group.TiltAngle = 0

    objects = {}
    build_base(doc, base_group, objects)
    build_pan_rotating(doc, pan_group, objects)
    build_tilt_rotating(doc, tilt_group, objects)
    add_references(doc, reference_group, objects)
    doc.recompute()

    validation = validate_geometry(doc, objects)
    write_docs(validation)

    fcstd_path = os.path.join(OUT_DIR, "pantilt_hc_v760_nema17_gt2.FCStd")
    step_path = os.path.join(OUT_DIR, "pantilt_hc_v760_nema17_gt2.step")
    doc.saveAs(fcstd_path)
    try:
        import Import

        Import.export(
            [
                obj
                for obj in doc.Objects
                if hasattr(obj, "Shape")
                and not obj.Shape.isNull()
                and not obj.Label.startswith("REFERENCE_")
            ],
            step_path,
        )
    except Exception as exc:
        App.Console.PrintWarning(f"STEP export failed: {exc}\n")

    print("WROTE", fcstd_path)
    if os.path.exists(step_path):
        print("WROTE", step_path)
    print("VALIDATION_PASSED", validation["passed"])
    print(json.dumps(validation, indent=2, sort_keys=True))
    return doc


if __name__ == "__main__":
    build()
