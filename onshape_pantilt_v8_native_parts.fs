FeatureScript 3070;
import(path : "onshape/std/geometry.fs", version : "3070.0");
export import(path : "onshape/std/tool.fs", version : "3070.0");

annotation { "Feature Type Name" : "PantiltV8NativePartsV2" }
export const pantiltV8NativePartsV2 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const mm = millimeter;
        const tiltAxisX = 10.3 * mm;
        const tiltAxisZ = 180 * mm;
        const panMotorX = -98 * mm;
        const panBeltZ = 52 * mm;
        const tiltBeltY = -45.8 * mm;
        const panPitchD = 120 * 2 / PI * mm;
        const tiltPitchD = 80 * 2 / PI * mm;
        const panMotorPitchD = 20 * 2 / PI * mm;
        const tiltMotorPitchD = 20 * 2 / PI * mm;

        buildBase(context, id + "base", panMotorX);
        buildPanOnePiece(context, id + "pan", tiltAxisX, tiltAxisZ, panBeltZ, panPitchD);
        buildTiltCradle(context, id + "tilt", tiltAxisX, tiltAxisZ, tiltBeltY, tiltPitchD);

        addNemaZ(context, id + "motor_pan_nema17", vector(panMotorX, 0 * mm, 90 * mm));
        addNemaY(context, id + "motor_tilt_nema17", vector(-35.7, -90.5, 108) * mm);
        addCylZNew(context, id + "pulley_pan_20T", vector(panMotorX, 0 * mm, panBeltZ), panMotorPitchD + 1.2 * mm, 10 * mm);
        addCylYNew(context, id + "pulley_tilt_20T", vector(-35.7 * mm, tiltBeltY, 108 * mm), tiltMotorPitchD + 1.2 * mm, 10 * mm);
        addCamera(context, id + "camera_hc_v760");
        addCylZNew(context, id + "bearing_51107_stack", vector(0, 0, 71) * mm, 52 * mm, 12 * mm);
        addCylZNew(context, id + "bearing_pan_608", vector(0, 0, 58) * mm, 22 * mm, 7 * mm);
        addCylYNew(context, id + "bearing_tilt_left_608", vector(tiltAxisX, 75.5 * mm, tiltAxisZ), 22 * mm, 7 * mm);
        addCylYNew(context, id + "bearing_tilt_right_608", vector(tiltAxisX, -66 * mm, tiltAxisZ), 22 * mm, 7 * mm);
    }, {});

function buildBase(context is Context, id is Id, panMotorX is ValueWithUnits)
{
    addCylZ(context, id + "_seed_center_disk", vector(0, 0, 5) * millimeter, 124 * millimeter, 10 * millimeter, NewBodyOperationType.NEW, qNothing());
    const part = solidCreatedBy(id + "_seed_center_disk");

    for (var i = 0; i < 3; i += 1)
    {
        const a = i * 120 * degree;
        const xDir = vector(cos(a), sin(a), 0);
        addBoxZ(context, id + ("_leg_" ~ i), vector(cos(a) * 86 * millimeter, sin(a) * 86 * millimeter, 5 * millimeter), 112 * millimeter, 28 * millimeter, 10 * millimeter, xDir, NewBodyOperationType.ADD, part);
        addCylZ(context, id + ("_foot_hole_" ~ i), vector(cos(a) * 128 * millimeter, sin(a) * 128 * millimeter, 5 * millimeter), 7.2 * millimeter, 14 * millimeter, NewBodyOperationType.REMOVE, part);
    }

    addCylZ(context, id + "_central_pedestal", vector(0, 0, 38) * millimeter, 54 * millimeter, 56 * millimeter, NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_pan_motor_foot", vector(-77, 0, 5) * millimeter, 90 * millimeter, 94 * millimeter, 10 * millimeter, vector(1, 0, 0), NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_pan_motor_top_arm", vector(panMotorX, 0 * millimeter, 63 * millimeter), 60 * millimeter, 94 * millimeter, 6 * millimeter, vector(1, 0, 0), NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_pan_motor_left_wall", vector(panMotorX, -44 * millimeter, 35 * millimeter), 60 * millimeter, 6 * millimeter, 50 * millimeter, vector(1, 0, 0), NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_pan_motor_right_wall", vector(panMotorX, 44 * millimeter, 35 * millimeter), 60 * millimeter, 6 * millimeter, 50 * millimeter, vector(1, 0, 0), NewBodyOperationType.ADD, part);

    addCylZ(context, id + "_cut_51107_lower_seat_52p4", vector(0, 0, 66) * millimeter, 52.4 * millimeter, 3 * millimeter, NewBodyOperationType.REMOVE, part);
    addCylZ(context, id + "_cut_pan_608_press_pocket_21p9", vector(0, 0, 58) * millimeter, 21.9 * millimeter, 16 * millimeter, NewBodyOperationType.REMOVE, part);
    addCylZ(context, id + "_cut_pan_motor_pilot_slot_visual", vector(panMotorX, 0 * millimeter, 63 * millimeter), 22.6 * millimeter, 8 * millimeter, NewBodyOperationType.REMOVE, part);
}

function buildPanOnePiece(context is Context, id is Id, tiltAxisX is ValueWithUnits, tiltAxisZ is ValueWithUnits, panBeltZ is ValueWithUnits, panPitchD is ValueWithUnits)
{
    addBoxZ(context, id + "_seed_square_platform_152", vector(0, 0, 80.5) * millimeter, 152 * millimeter, 152 * millimeter, 7 * millimeter, vector(1, 0, 0), NewBodyOperationType.NEW, qNothing());
    const part = solidCreatedBy(id + "_seed_square_platform_152");

    addCylZ(context, id + "_connector_skirt", vector(0, 0, 66.55) * millimeter, 82 * millimeter, 19.5 * millimeter, NewBodyOperationType.ADD, part);
    addCylZ(context, id + "_integral_120T_GT2_blank", vector(0 * millimeter, 0 * millimeter, panBeltZ), panPitchD - 0.2 * millimeter, 10 * millimeter, NewBodyOperationType.ADD, part);
    addCylZ(context, id + "_thrust_hub_34p6", vector(0, 0, 70.5) * millimeter, 34.6 * millimeter, 10.4 * millimeter, NewBodyOperationType.ADD, part);
    addCylZ(context, id + "_journal_7p9", vector(0, 0, 65.8) * millimeter, 7.9 * millimeter, 15.4 * millimeter, NewBodyOperationType.ADD, part);

    addBoxY(context, id + "_left_yoke_base", vector(-12, 71, 90) * millimeter, 128 * millimeter, 10 * millimeter, 14 * millimeter, NewBodyOperationType.ADD, part);
    addBoxY(context, id + "_left_yoke_lcd_routed_arm", vector(-30, 71, 136) * millimeter, 34 * millimeter, 10 * millimeter, 86 * millimeter, NewBodyOperationType.ADD, part);
    addBoxY(context, id + "_right_yoke_direct_motor_plate", vector(-12, -61.5, 143) * millimeter, 128 * millimeter, 10 * millimeter, 118 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_left_608_boss", vector(tiltAxisX, 71 * millimeter, tiltAxisZ), 38 * millimeter, 16 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_right_608_boss", vector(tiltAxisX, -61.5 * millimeter, tiltAxisZ), 38 * millimeter, 16 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_cut_left_bearing_pocket_22p12", vector(tiltAxisX, 75.5 * millimeter, tiltAxisZ), 22.12 * millimeter, 9 * millimeter, NewBodyOperationType.REMOVE, part);
    addCylY(context, id + "_cut_right_bearing_pocket_22p12", vector(tiltAxisX, -66 * millimeter, tiltAxisZ), 22.12 * millimeter, 9 * millimeter, NewBodyOperationType.REMOVE, part);
    addCylZ(context, id + "_cut_120T_bore_58", vector(0 * millimeter, 0 * millimeter, panBeltZ), 58 * millimeter, 34 * millimeter, NewBodyOperationType.REMOVE, part);
    addCylZ(context, id + "_cut_upper_51107_seat_52p4", vector(0, 0, 76.5) * millimeter, 52.4 * millimeter, 3 * millimeter, NewBodyOperationType.REMOVE, part);
}

function buildTiltCradle(context is Context, id is Id, tiltAxisX is ValueWithUnits, tiltAxisZ is ValueWithUnits, tiltBeltY is ValueWithUnits, tiltPitchD is ValueWithUnits)
{
    addBoxZ(context, id + "_seed_camera_saddle_39x98", vector(10, 10, 140) * millimeter, 39 * millimeter, 98 * millimeter, 5 * millimeter, vector(1, 0, 0), NewBodyOperationType.NEW, qNothing());
    const part = solidCreatedBy(id + "_seed_camera_saddle_39x98");

    addBoxY(context, id + "_right_cheek", vector(tiltAxisX, -37 * millimeter, 161 * millimeter), 60 * millimeter, 6 * millimeter, 44 * millimeter, NewBodyOperationType.ADD, part);
    addBoxY(context, id + "_left_cheek", vector(tiltAxisX, 57 * millimeter, 161 * millimeter), 32 * millimeter, 6 * millimeter, 44 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_right_hub", vector(tiltAxisX, -37 * millimeter, tiltAxisZ), 26 * millimeter, 8 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_left_hub", vector(tiltAxisX, 57 * millimeter, tiltAxisZ), 26 * millimeter, 8 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_left_trunnion_7p9", vector(tiltAxisX, 71.5 * millimeter, tiltAxisZ), 7.9 * millimeter, 25 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_right_trunnion_7p9", vector(tiltAxisX, -61.25 * millimeter, tiltAxisZ), 7.9 * millimeter, 22.5 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_integral_80T_GT2_blank", vector(tiltAxisX, tiltBeltY, tiltAxisZ), tiltPitchD - 0.2 * millimeter, 10 * millimeter, NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_cut_camera_screw_slot", vector(10, 0, 140) * millimeter, 28 * millimeter, 7 * millimeter, 8 * millimeter, vector(1, 0, 0), NewBodyOperationType.REMOVE, part);
    addCylY(context, id + "_cut_80T_bore_8", vector(tiltAxisX, tiltBeltY, tiltAxisZ), 8 * millimeter, 14 * millimeter, NewBodyOperationType.REMOVE, part);
}

function addCamera(context is Context, id is Id)
{
    addBoxNew(context, id + "_body", vector(0, 0, 179) * millimeter, 139 * millimeter, 65 * millimeter, 73 * millimeter);
    const part = solidCreatedBy(id + "_body");
    addCylX(context, id + "_lens", vector(74.5, 0, 181) * millimeter, 36 * millimeter, 30 * millimeter, NewBodyOperationType.ADD, part);
    addBoxZ(context, id + "_rear_battery", vector(-70.5, 0, 179) * millimeter, 30 * millimeter, 48 * millimeter, 52 * millimeter, vector(1, 0, 0), NewBodyOperationType.ADD, part);
}

function addNemaZ(context is Context, id is Id, center is Vector)
{
    addBoxNew(context, id + "_body", center, 42 * millimeter, 42 * millimeter, 48 * millimeter);
    const part = solidCreatedBy(id + "_body");
    addCylZ(context, id + "_pilot", center - vector(0, 0, 24.5) * millimeter, 22 * millimeter, 3 * millimeter, NewBodyOperationType.ADD, part);
    addCylZ(context, id + "_shaft", center - vector(0, 0, 35) * millimeter, 5 * millimeter, 24 * millimeter, NewBodyOperationType.ADD, part);
}

function addNemaY(context is Context, id is Id, center is Vector)
{
    addBoxNew(context, id + "_body", center, 42 * millimeter, 48 * millimeter, 42 * millimeter);
    const part = solidCreatedBy(id + "_body");
    addCylY(context, id + "_pilot", center + vector(0, 24.5, 0) * millimeter, 22 * millimeter, 3 * millimeter, NewBodyOperationType.ADD, part);
    addCylY(context, id + "_shaft", center + vector(0, 35, 0) * millimeter, 5 * millimeter, 24 * millimeter, NewBodyOperationType.ADD, part);
}

function solidCreatedBy(id is Id) returns Query
{
    return qBodyType(qCreatedBy(id, EntityType.BODY), BodyType.SOLID);
}

function addBoxNew(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits)
{
    addBoxZ(context, id, center, sx, sy, sz, vector(1, 0, 0), NewBodyOperationType.NEW, qNothing());
}

function addCylZNew(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits)
{
    addCylZ(context, id, center, diameter, height, NewBodyOperationType.NEW, qNothing());
}

function addCylYNew(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits)
{
    addCylY(context, id, center, diameter, height, NewBodyOperationType.NEW, qNothing());
}

function addBoxZ(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits, xDir is Vector, opType is NewBodyOperationType, scope is Query)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, 0 * millimeter, sz / 2), vector(0, 0, 1), xDir) });
    skRectangle(sketch, "profile", { "firstCorner" : vector(-sx / 2, -sy / 2), "secondCorner" : vector(sx / 2, sy / 2) });
    skSolve(sketch);
    doExtrude(context, id, sketchId, vector(0, 0, 1), sz, opType, scope);
}

function addBoxY(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits, opType is NewBodyOperationType, scope is Query)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, sy / 2, 0 * millimeter), vector(0, 1, 0), vector(1, 0, 0)) });
    skRectangle(sketch, "profile", { "firstCorner" : vector(-sx / 2, -sz / 2), "secondCorner" : vector(sx / 2, sz / 2) });
    skSolve(sketch);
    doExtrude(context, id, sketchId, vector(0, 1, 0), sy, opType, scope);
}

function addCylZ(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits, opType is NewBodyOperationType, scope is Query)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, 0 * millimeter, height / 2), vector(0, 0, 1), vector(1, 0, 0)) });
    skCircle(sketch, "profile", { "center" : vector(0, 0) * millimeter, "radius" : diameter / 2 });
    skSolve(sketch);
    doExtrude(context, id, sketchId, vector(0, 0, 1), height, opType, scope);
}

function addCylY(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits, opType is NewBodyOperationType, scope is Query)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, height / 2, 0 * millimeter), vector(0, 1, 0), vector(1, 0, 0)) });
    skCircle(sketch, "profile", { "center" : vector(0, 0) * millimeter, "radius" : diameter / 2 });
    skSolve(sketch);
    doExtrude(context, id, sketchId, vector(0, 1, 0), height, opType, scope);
}

function addCylX(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits, opType is NewBodyOperationType, scope is Query)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(height / 2, 0 * millimeter, 0 * millimeter), vector(1, 0, 0), vector(0, 1, 0)) });
    skCircle(sketch, "profile", { "center" : vector(0, 0) * millimeter, "radius" : diameter / 2 });
    skSolve(sketch);
    doExtrude(context, id, sketchId, vector(1, 0, 0), height, opType, scope);
}

function doExtrude(context is Context, id is Id, sketchId is Id, direction is Vector, depth is ValueWithUnits, opType is NewBodyOperationType, scope is Query)
{
    if (opType == NewBodyOperationType.NEW)
    {
        extrude(context, id, { "entities" : qSketchRegion(sketchId), "direction" : direction, "endBound" : BoundingType.BLIND, "depth" : depth, "operationType" : opType });
    }
    else
    {
        extrude(context, id, { "entities" : qSketchRegion(sketchId), "direction" : direction, "endBound" : BoundingType.BLIND, "depth" : depth, "operationType" : opType, "defaultScope" : false, "booleanScope" : scope });
    }
}
