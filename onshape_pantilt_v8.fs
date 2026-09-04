FeatureScript 3070;
import(path : "onshape/std/geometry.fs", version : "3070.0");

annotation { "Feature Type Name" : "PantiltV8CleanAssembly" }
export const pantiltV8CleanAssembly = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const mm = millimeter;

        const panMotorX = -98 * mm;
        const panBeltZ = 52 * mm;
        const tiltAxisX = 10.3 * mm;
        const tiltAxisZ = 180 * mm;
        const tiltMotorX = -35.7 * mm;
        const tiltMotorZ = 108 * mm;
        const tiltBeltY = -45.8 * mm;
        const panPitchD = 120 * 2 / PI * mm;
        const panMotorPitchD = 20 * 2 / PI * mm;
        const tiltPitchD = 80 * 2 / PI * mm;
        const tiltMotorPitchD = 20 * 2 / PI * mm;

        addBaseEnvelope(context, id + "PRINT_base_three_leg_51107_608_downshaft");
        addPanEnvelope(context, id + "PRINT_one_piece_pan_platform_yokes_journal_120T", tiltAxisX, tiltAxisZ, panPitchD);
        addTiltEnvelope(context, id + "PRINT_one_piece_tilt_cradle_trunnions_80T", tiltAxisX, tiltAxisZ, tiltBeltY, tiltPitchD);

        addNemaZ(context, id + "MOTOR_pan_NEMA17_shaft_down", vector(panMotorX, 0 * mm, 90 * mm));
        addNemaY(context, id + "MOTOR_tilt_NEMA17_direct_mount", vector(tiltMotorX, -90.5 * mm, tiltMotorZ));

        addCylinderZ(context, id + "PULLEY_pan_motor_20T", vector(panMotorX, 0 * mm, panBeltZ), panMotorPitchD + 1.2 * mm, 10 * mm);
        addCylinderY(context, id + "PULLEY_tilt_motor_20T", vector(tiltMotorX, tiltBeltY, tiltMotorZ), tiltMotorPitchD + 1.2 * mm, 10 * mm);

        addCylinderZ(context, id + "BEARING_pan_51107_stack_35x52x12", vector(0, 0, 71) * mm, 52 * mm, 12 * mm);
        addCylinderZ(context, id + "BEARING_pan_608_radial_8x22x7", vector(0, 0, 58) * mm, 22 * mm, 7 * mm);
        addCylinderY(context, id + "BEARING_tilt_left_608", vector(tiltAxisX, 75.5 * mm, tiltAxisZ), 22 * mm, 7 * mm);
        addCylinderY(context, id + "BEARING_tilt_right_608", vector(tiltAxisX, -66 * mm, tiltAxisZ), 22 * mm, 7 * mm);

        addBeltZSimple(context, id + "BELT_pan_GT2_10mm_approx_350", panMotorX, panBeltZ, panMotorPitchD, panPitchD);
        addBeltYSimple(context, id + "BELT_tilt_GT2_10mm_approx_280", tiltMotorX, tiltMotorZ, tiltBeltY, tiltAxisX, tiltAxisZ, tiltMotorPitchD, tiltPitchD);

        addCameraEnvelope(context, id + "CAMERA_HC_V760_envelope");
        addBox(context, id + "CLEARANCE_lcd_open", vector(35, 66.5, 179) * mm, 4 * mm, 68 * mm, 45 * mm);
        addBox(context, id + "CLEARANCE_hdmi_20mm", vector(10.3, 42.5, 169) * mm, 24 * mm, 20 * mm, 16 * mm);

        addCylinderZ(context, id + "REFERENCE_pan_axis", vector(0, 0, 117.5) * mm, 2 * mm, 235 * mm);
        addCylinderY(context, id + "REFERENCE_tilt_axis", vector(tiltAxisX, 0 * mm, tiltAxisZ), 2 * mm, 170 * mm);
    }, {});

function addBaseEnvelope(context is Context, id is Id)
{
    addCylinderZ(context, id + "_center_pedestal", vector(0, 0, 36) * millimeter, 62 * millimeter, 62 * millimeter);
    for (var i = 0; i < 3; i += 1)
    {
        const a = i * 120 * degree;
        addBoxRz(context, id + ("_leg_" ~ i), vector(cos(a) * 84 * millimeter, sin(a) * 84 * millimeter, 5 * millimeter), 118 * millimeter, 28 * millimeter, 10 * millimeter, a);
    }
    addBox(context, id + "_pan_motor_bridge", vector(-98, 0, 38) * millimeter, 70 * millimeter, 94 * millimeter, 62 * millimeter);
}

function addPanEnvelope(context is Context, id is Id, tiltAxisX is ValueWithUnits, tiltAxisZ is ValueWithUnits, panPitchD is ValueWithUnits)
{
    addBox(context, id + "_square_top_152", vector(0, 0, 80.5) * millimeter, 152 * millimeter, 152 * millimeter, 7 * millimeter);
    addCylinderZ(context, id + "_lower_skirt_and_120T", vector(0, 0, 59) * millimeter, panPitchD, 25 * millimeter);
    addCylinderZ(context, id + "_journal_7p9_and_thrust_hub", vector(0, 0, 67) * millimeter, 34.6 * millimeter, 22 * millimeter);
    addBox(context, id + "_left_yoke_lcd_routed", vector(-18, 71, 136) * millimeter, 118 * millimeter, 10 * millimeter, 92 * millimeter);
    addBox(context, id + "_right_yoke_direct_motor", vector(-12, -61.5, 143) * millimeter, 128 * millimeter, 10 * millimeter, 118 * millimeter);
    addCylinderY(context, id + "_left_tilt_boss", vector(tiltAxisX, 71 * millimeter, tiltAxisZ), 38 * millimeter, 16 * millimeter);
    addCylinderY(context, id + "_right_tilt_boss", vector(tiltAxisX, -61.5 * millimeter, tiltAxisZ), 38 * millimeter, 16 * millimeter);
}

function addTiltEnvelope(context is Context, id is Id, tiltAxisX is ValueWithUnits, tiltAxisZ is ValueWithUnits, tiltBeltY is ValueWithUnits, tiltPitchD is ValueWithUnits)
{
    addBox(context, id + "_camera_saddle_39x98", vector(10, 10, 140) * millimeter, 39 * millimeter, 98 * millimeter, 5 * millimeter);
    addBox(context, id + "_cradle_body", vector(10.3, 10, 162) * millimeter, 64 * millimeter, 100 * millimeter, 44 * millimeter);
    addCylinderY(context, id + "_left_trunnion_7p9", vector(tiltAxisX, 71.5 * millimeter, tiltAxisZ), 7.9 * millimeter, 25 * millimeter);
    addCylinderY(context, id + "_right_trunnion_7p9", vector(tiltAxisX, -61.25 * millimeter, tiltAxisZ), 7.9 * millimeter, 22.5 * millimeter);
    addCylinderY(context, id + "_integral_80T_GT2", vector(tiltAxisX, tiltBeltY, tiltAxisZ), tiltPitchD, 10 * millimeter);
}

function addCameraEnvelope(context is Context, id is Id)
{
    addBox(context, id + "_body", vector(0, 0, 179) * millimeter, 139 * millimeter, 65 * millimeter, 73 * millimeter);
    addCylinderX(context, id + "_lens", vector(79.5, 0, 181) * millimeter, 36 * millimeter, 20 * millimeter);
    addBox(context, id + "_rear_battery", vector(-76.5, 0, 179) * millimeter, 18 * millimeter, 48 * millimeter, 52 * millimeter);
}

function addNemaZ(context is Context, id is Id, center is Vector)
{
    addBox(context, id + "_body", center, 42 * millimeter, 42 * millimeter, 48 * millimeter);
    addCylinderZ(context, id + "_pilot", center - vector(0, 0, 25) * millimeter, 22 * millimeter, 2 * millimeter);
    addCylinderZ(context, id + "_shaft", center - vector(0, 0, 36) * millimeter, 5 * millimeter, 24 * millimeter);
}

function addNemaY(context is Context, id is Id, center is Vector)
{
    addBox(context, id + "_body", center, 42 * millimeter, 48 * millimeter, 42 * millimeter);
    addCylinderY(context, id + "_pilot", center + vector(0, 25, 0) * millimeter, 22 * millimeter, 2 * millimeter);
    addCylinderY(context, id + "_shaft", center + vector(0, 36, 0) * millimeter, 5 * millimeter, 24 * millimeter);
}

function addBeltZSimple(context is Context, id is Id, motorX is ValueWithUnits, z is ValueWithUnits, motorD is ValueWithUnits, drivenD is ValueWithUnits)
{
    addCylinderZ(context, id + "_motor_wrap", vector(motorX, 0 * millimeter, z), motorD + 2 * millimeter, 10 * millimeter);
    addCylinderZ(context, id + "_driven_wrap", vector(0 * millimeter, 0 * millimeter, z), drivenD + 2 * millimeter, 10 * millimeter);
    addBox(context, id + "_front_run", vector(-49, 40, 52) * millimeter, 98 * millimeter, 2 * millimeter, 10 * millimeter);
    addBox(context, id + "_rear_run", vector(-49, -40, 52) * millimeter, 98 * millimeter, 2 * millimeter, 10 * millimeter);
}

function addBeltYSimple(context is Context, id is Id, motorX is ValueWithUnits, motorZ is ValueWithUnits, y is ValueWithUnits, drivenX is ValueWithUnits, drivenZ is ValueWithUnits, motorD is ValueWithUnits, drivenD is ValueWithUnits)
{
    addCylinderY(context, id + "_motor_wrap", vector(motorX, y, motorZ), motorD + 2 * millimeter, 10 * millimeter);
    addCylinderY(context, id + "_driven_wrap", vector(drivenX, y, drivenZ), drivenD + 2 * millimeter, 10 * millimeter);
    addBox(context, id + "_upper_run", vector(-12 * millimeter, y, 147 * millimeter), 58 * millimeter, 10 * millimeter, 2 * millimeter);
    addBox(context, id + "_lower_run", vector(-12 * millimeter, y, 140 * millimeter), 58 * millimeter, 10 * millimeter, 2 * millimeter);
}

function addBox(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, 0 * millimeter, sz / 2), vector(0, 0, 1)) });
    skRectangle(sketch, "profile", { "firstCorner" : vector(-sx / 2, -sy / 2), "secondCorner" : vector(sx / 2, sy / 2) });
    skSolve(sketch);
    opExtrude(context, id, { "entities" : qSketchRegion(sketchId), "direction" : vector(0, 0, 1), "endBound" : BoundingType.BLIND, "endDepth" : sz });
}

function addBoxRz(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits, angle is ValueWithUnits)
{
    addBox(context, id, vector(0, 0, 0) * millimeter, sx, sy, sz);
    opTransform(context, id + "move", { "bodies" : qCreatedBy(id, EntityType.BODY), "transform" : transform(center) * rotationAround(line(vector(0, 0, 0) * millimeter, vector(0, 0, 1)), angle) });
}

function addCylinderZ(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, 0 * millimeter, height / 2), vector(0, 0, 1)) });
    skCircle(sketch, "profile", { "center" : vector(0, 0) * millimeter, "radius" : diameter / 2 });
    skSolve(sketch);
    opExtrude(context, id, { "entities" : qSketchRegion(sketchId), "direction" : vector(0, 0, 1), "endBound" : BoundingType.BLIND, "endDepth" : height });
}

function addCylinderY(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits)
{
    addCylinderZ(context, id, vector(0, 0, 0) * millimeter, diameter, height);
    opTransform(context, id + "turnY", { "bodies" : qCreatedBy(id, EntityType.BODY), "transform" : transform(center - vector(0 * millimeter, height / 2, 0 * millimeter)) * rotationAround(line(vector(0, 0, 0) * millimeter, vector(1, 0, 0)), -90 * degree) });
}

function addCylinderX(context is Context, id is Id, center is Vector, diameter is ValueWithUnits, height is ValueWithUnits)
{
    addCylinderZ(context, id, vector(0, 0, 0) * millimeter, diameter, height);
    opTransform(context, id + "turnX", { "bodies" : qCreatedBy(id, EntityType.BODY), "transform" : transform(center - vector(height / 2, 0 * millimeter, 0 * millimeter)) * rotationAround(line(vector(0, 0, 0) * millimeter, vector(0, 1, 0)), 90 * degree) });
}
