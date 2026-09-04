---
goal: Integral One-Piece Tilt Cradle V3
version: 3.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Completed'
tags: [design, architecture, freecad, mechanical, pan-tilt]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Replace the continuous tilt axle and separate driven pulley with one printed rotating tilt part. The camera cradle, both side cheeks, two short plastic trunnions, and the 80T driven pulley must form one connected solid while leaving the camera volume free of any cross-shaft.

## 1. Requirements & Constraints

- **REQ-001**: Remove the continuous steel tilt axle and every separate axle collar from the generated assembly.
- **REQ-002**: Generate exactly one printed `Part::Feature` for the camera plate, both cheeks, both bearing trunnions, hubs, and 80T driven pulley.
- **REQ-003**: Require the integral tilt feature to contain exactly one connected solid.
- **REQ-004**: Use two short 7.9 mm plastic trunnions running only from each cradle cheek into the corresponding 608 bearing.
- **REQ-005**: Keep the complete camera envelope free of a cross-shaft between the two cradle cheeks.
- **REQ-006**: Integrate the 80T pulley on the outboard side of the right trunnion and retain the existing external GT2 belt plane.
- **REQ-007**: Keep both 608 bearings seated in the existing pan yoke and leave the pan mechanism unchanged.
- **REQ-008**: Preserve the balanced camera position, mounting slot, nominal camera envelope, and -60/0/+60 degree tilt clearance.
- **REQ-009**: Regenerate FCStd, STEP, BOM, CAD checks, machine-readable validation, v3 screenshots, and a comparison sheet using all three reference photographs.
- **CON-001**: Treat plastic journal diameter, bearing fit, creep, wear, layer orientation, and exact GT2 tooth geometry as prototype-dependent production details.
- **CON-002**: Preserve v2 under `/home/user/pantilt/legacy_v2_axle_20260827/`.
- **GUD-001**: Continue using the deterministic FreeCAD 1.1.3 Python generator and existing pan architecture.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Replace the tilt load path without changing pan.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up the v2 generator, model, STEP, reports, and screenshots. | yes | 2026-08-27 |
| TASK-002 | Remove the separate 80T pulley, continuous steel axle, collar, plate, cheeks, and hubs. | yes | 2026-08-27 |
| TASK-003 | Fuse the plate, cheeks, solid hubs, short trunnions, 80T body, flanges, and 80 teeth into one printed feature. | yes | 2026-08-27 |
| TASK-004 | Add validation fields for one feature, one solid, and no through-shaft. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Regenerate and visually verify v3.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-005 | Generate FCStd and STEP and require all B-reps to be valid. | yes | 2026-08-27 |
| TASK-006 | Require zero selected interference and zero pose interference at -60, 0, and +60 degrees. | yes | 2026-08-27 |
| TASK-007 | Render the ten-view v3 screenshot set and inspect the shaft-free camera volume and integral pulley. | yes | 2026-08-27 |
| TASK-008 | Generate and inspect the v3 comparison sheet against all three supplied references. | yes | 2026-08-27 |
| TASK-009 | Update README, BOM, CAD checks, and complete this plan. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: A shorter separate steel shaft was rejected because the user explicitly requires the complete tilt mechanism to be one printed part.
- **ALT-002**: A separately fastened 80T pulley was rejected because it would violate the one-piece requirement and add a hub interface.
- **ALT-003**: An inboard pulley was rejected because it would consume camera clearance and diverge from the external belt architecture visible in the reference.

## 4. Dependencies

- **DEP-001**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-002**: `/home/user/Applications/FreeCAD-1.1.3.AppImage` for GUI screenshot generation.
- **DEP-003**: Local FFmpeg for the reference comparison sheet.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - authoritative v3 geometry generator.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v3 rendering and motion-pose generator.
- **FILE-003**: `/home/user/pantilt/README.md` - architecture and production limitations.
- **FILE-004**: `/home/user/pantilt/BOM.md` - generated v3 concept bill of materials.
- **FILE-005**: `/home/user/pantilt/cad_checks.md` - generated dimensions and validation summary.
- **FILE-006**: `/home/user/pantilt/geometry_validation.json` - machine-readable v3 checks.

## 6. Testing

- **TEST-001**: Run `/home/user/pantilt/generate_pantilt_freecad.sh` and require exit code 0.
- **TEST-002**: Require `TILT_ROTATING_one_piece_cradle_trunnions_80T` to exist once and contain exactly one solid.
- **TEST-003**: Require no object label matching the removed continuous tilt axle.
- **TEST-004**: Require all generated B-reps to be valid and every selected interference volume to be at most 0.01 mm3.
- **TEST-005**: Require zero camera/cradle interference at tilt angles -60, 0, and +60 degrees.
- **TEST-006**: Require every v3 screenshot to be a non-empty 1600x1200 PNG and visually inspect the final comparison sheet.

## 7. Risks & Assumptions

- **RISK-001**: Printed trunnions running directly in 608 inner races may creep or wear and need a sacrificial sleeve or revised fit after prototyping.
- **RISK-002**: Fusing 80 visual teeth into the main body can create a heavier B-rep and remains an approximation of the GT2 profile.
- **RISK-003**: The camera placeholder omits exact battery, LCD hinge, connector, and cable geometry.
- **ASSUMPTION-001**: The integral pulley belongs outside the right bearing and remains connected through the short right trunnion, matching the visible reference belt path.
- **ASSUMPTION-002**: The existing pan assembly is accepted provisionally and must not be redesigned in this revision.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/plan/design-pan-tilt-reference-v2.md`

`/home/user/pantilt/legacy_v2_axle_20260827/cad_checks.md`
