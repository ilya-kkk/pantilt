FeatureScript 3070;
import(path : "onshape/std/geometry.fs", version : "3070.0");

annotation { "Feature Type Name" : "PantiltV8FewPartAssembly" }
export const pantiltV8FewPartAssembly = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const mm = millimeter;
        const tiltAxisX = 10.3 * mm;
        const tiltAxisZ = 180 * mm;

        addCylinderZ(context, id + "PRINT_base_51107_608_pan_motor_mount", vector(0, 0, 36) * mm, 168 * mm, 72 * mm);
        addBox(context, id + "PRINT_one_piece_pan_platform_yokes_120T_journal", vector(-10, 0, 132) * mm, 170 * mm, 152 * mm, 112 * mm);
        addBox(context, id + "PRINT_one_piece_tilt_cradle_trunnions_80T", vector(10.3, 10, 160) * mm, 82 * mm, 112 * mm, 58 * mm);

        addBox(context, id + "CAMERA_HC_V760_envelope", vector(0, 0, 179) * mm, 139 * mm, 65 * mm, 73 * mm);
        addBox(context, id + "MOTOR_pan_NEMA17_shaft_down", vector(-98, 0, 90) * mm, 42 * mm, 42 * mm, 48 * mm);
        addBox(context, id + "MOTOR_tilt_NEMA17_direct_mount", vector(-35.7, -90.5, 108) * mm, 42 * mm, 48 * mm, 42 * mm);

        addCylinderZ(context, id + "BELT_pan_GT2_approx_350", vector(-49, 0, 52) * mm, 116 * mm, 10 * mm);
        addCylinderY(context, id + "BELT_tilt_GT2_approx_280", vector(-12 * mm, -45.8 * mm, 146 * mm), 72 * mm, 10 * mm);

        addCylinderZ(context, id + "REFERENCE_pan_axis", vector(0, 0, 117.5) * mm, 2 * mm, 235 * mm);
        addCylinderY(context, id + "REFERENCE_tilt_axis", vector(tiltAxisX, 0 * mm, tiltAxisZ), 2 * mm, 170 * mm);
    }, {});

function addBox(context is Context, id is Id, center is Vector, sx is ValueWithUnits, sy is ValueWithUnits, sz is ValueWithUnits)
{
    const sketchId = id + "sk";
    var sketch = newSketchOnPlane(context, sketchId, { "sketchPlane" : plane(center - vector(0 * millimeter, 0 * millimeter, sz / 2), vector(0, 0, 1)) });
    skRectangle(sketch, "profile", { "firstCorner" : vector(-sx / 2, -sy / 2), "secondCorner" : vector(sx / 2, sy / 2) });
    skSolve(sketch);
    opExtrude(context, id, { "entities" : qSketchRegion(sketchId), "direction" : vector(0, 0, 1), "endBound" : BoundingType.BLIND, "endDepth" : sz });
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
