---
goal: Direct Tilt Motor Mount V6
version: 6.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Completed'
tags: [design, freecad, mechanical, nema17, belt-tension]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Remove the separate tilt motor slide plate and standoffs. Mount the selected NEMA17 directly against the outside face of the right pan yoke, with the motor pilot and four M3 fasteners sliding vertically in the yoke itself for belt tension adjustment.

## 1. Requirements & Constraints

- **REQ-001**: Use the StepperOnline 17HS19-2004S1 envelope: 42x42x48 mm body, 5x24 mm shaft, 22 mm concentric pilot, and 31 mm mounting square.
- **REQ-002**: Seat the motor front face directly against the outside surface of the right pan yoke with no spacer plate or standoffs.
- **REQ-003**: Cut a vertical racetrack opening for the 22 mm pilot with clearance over the complete tensioning travel.
- **REQ-004**: Cut four parallel vertical M3 clearance slots on the 31 mm square with the same tensioning travel.
- **REQ-005**: Keep the 20T motor pulley in the existing tilt belt plane and within the 24 mm shaft reach.
- **REQ-006**: Preserve the one-piece tilt cradle, real 80T GT2/2MR profile, bearings, no-through-shaft architecture, and camera clearances.
- **REQ-007**: Require zero volume interference between the right yoke and motor body, pilot, shaft, and pulley.
- **REQ-008**: Regenerate FCStd, STEP, standalone tilt STEP/STL, reports, v6 screenshots, and reference comparison.
- **CON-001**: Do not redesign the pan bearing or pan belt drive in this revision.
- **CON-002**: Preserve v5 under `/home/user/pantilt/legacy_v5_printable_gt2_20260827/`.
- **GUD-001**: Keep the deterministic FreeCAD 1.1.3 Python workflow.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Integrate the motor interface into the pan yoke.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up v5 source, CAD, print exports, reports, plan, and screenshots. | yes | 2026-08-27 |
| TASK-002 | Add the pilot diameter, height, shaft length, and tension travel as explicit parameters. | yes | 2026-08-27 |
| TASK-003 | Cut the pilot racetrack and four M3 tensioning slots into the right yoke. | yes | 2026-08-27 |
| TASK-004 | Remove the separate slide plate and four standoffs. | yes | 2026-08-27 |
| TASK-005 | Move the motor, pilot, and shaft against the yoke outer face while keeping pulley alignment. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Validate and document v6.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-006 | Add direct-mount topology, shaft reach, and yoke-clearance checks. | yes | 2026-08-27 |
| TASK-007 | Rebuild all CAD and print artifacts and require one valid integral tilt solid. | yes | 2026-08-27 |
| TASK-008 | Require zero static and -60/0/+60 degree pose interference. | yes | 2026-08-27 |
| TASK-009 | Render and inspect v6 motor-mount, assembly, and comparison views. | yes | 2026-08-27 |
| TASK-010 | Update README, BOM, CAD checks, and mark this plan complete. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: Retaining the separate slide was rejected because it adds compliance, overhang, and parts without providing a function the yoke cannot perform.
- **ALT-002**: A round stationary pilot hole was rejected because the motor pilot would block vertical belt adjustment.
- **ALT-003**: Slots only for the screws were rejected because the concentric pilot must move by the same amount as the fasteners.

## 4. Dependencies

- **DEP-001**: StepperOnline 17HS19-2004S1 product drawing and STEP model.
- **DEP-002**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-003**: `/home/user/Applications/FreeCAD-1.1.3.AppImage` for screenshots.
- **DEP-004**: Local FFmpeg for the comparison sheet.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - direct mount geometry and validation.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v6 screenshot generation.
- **FILE-003**: `/home/user/pantilt/geometry_validation.json` - direct mount and collision checks.
- **FILE-004**: `/home/user/pantilt/pantilt_hc_v760_nema17_gt2.FCStd` - complete v6 assembly.
- **FILE-005**: `/home/user/pantilt/README.md` - architecture and production notes.
- **FILE-006**: `/home/user/pantilt/right_pan_yoke_direct_nema17.step` - standalone direct-mount yoke.
- **FILE-007**: `/home/user/pantilt/right_pan_yoke_direct_nema17.stl` - printable direct-mount yoke.

## 6. Testing

- **TEST-001**: Run `/home/user/pantilt/generate_pantilt_freecad.sh` and require exit code 0 and `VALIDATION_PASSED True`.
- **TEST-002**: Require slide and standoff feature counts to be zero and direct-mount slot count to equal five.
- **TEST-003**: Require at least 0.3 mm diametral pilot clearance and positive shaft engagement into the 20T pulley.
- **TEST-004**: Require all selected intersections, including yoke versus motor body/pilot/shaft/pulley, to be at most 0.01 mm3.
- **TEST-005**: Require valid B-reps, one integral tilt solid, and zero pose interference at -60, 0, and +60 degrees.
- **TEST-006**: Require non-empty v6 screenshots and original-resolution visual inspection of the direct mount.

## 7. Risks & Assumptions

- **RISK-001**: The remaining plastic around the lower-right motor slot must be checked after slicing for adequate perimeters and layer orientation.
- **RISK-002**: The selected motor's 24 mm shaft only provides limited pulley hub engagement after crossing the yoke wall.
- **RISK-003**: Belt tension must be set without forcing the pilot against the end of its racetrack opening.
- **ASSUMPTION-001**: The production motor is StepperOnline 17HS19-2004S1 or has an equivalent 42 mm NEMA17 face and 24 mm shaft.
- **ASSUMPTION-002**: Vertical motor travel is sufficient for assembly and tensioning of the selected closed-loop belt.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/plan/design-printable-gt2-2mr-pulley-v5.md`

`https://www.omc-stepperonline.com/nema-17-bipolar-59ncm-84oz-in-2a-42x48mm-4-wires-w-1m-cable-connector-17hs19-2004s1`
