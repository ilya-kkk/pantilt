---
goal: Short HDMI Clearance Cradle V7
version: 7.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Complete'
tags: [design, freecad, mechanical, camera, hdmi, lcd]
---

# Introduction

![Status: Complete](https://img.shields.io/badge/status-Complete-green)

Replace the full-length camera platform with a short saddle centered near the measured HC-V760 center of mass. Add 20 mm of one-sided clearance on the camera-left LCD/HDMI side and widen the corresponding pan structure while preserving the accepted drive architecture.

## 1. Requirements & Constraints

- **REQ-001**: Leave the camera unsupported for 40 mm at the front and 60 mm at the rear, producing a 39 mm platform for the 139 mm camera envelope.
- **REQ-002**: Position the platform from X=-9.5 to X=29.5 mm, centered at X=10.0 mm.
- **REQ-003**: Model the camera center of mass 1.9 NEMA17 widths from the rear: X=10.3 mm, and align the tilt axis to it.
- **REQ-004**: Add 20 mm clearance only on the camera-left side for the LCD hinge and Micro HDMI cable.
- **REQ-005**: Increase the plate width from 78 to 98 mm, shifting its center 10 mm left so the opposite edge stays unchanged.
- **REQ-006**: Move the left tilt cheek, trunnion, 608 support, yoke, and pan support outward by 20 mm; leave the right drive side unchanged.
- **REQ-007**: Provide at least 20 mm between the camera-left body face and the inner face of the printed tilt cheek.
- **REQ-008**: Add explicit open-LCD and 20 mm HDMI cable clearance references and require zero solid interference with the printed cradle/yoke in the nominal pose.
- **REQ-009**: Preserve the integral GT2/2MR pulley, direct NEMA17 mount, bearing arrangement, and -60/0/+60 degree motion checks.
- **CON-001**: Camera body remains a 139x65x73 mm measured placeholder until a full physical scan is available.
- **CON-002**: Preserve v6 under `/home/user/pantilt/legacy_v6_direct_motor_20260827/`.
- **GUD-001**: Keep the deterministic FreeCAD 1.1.3 workflow.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Build the short asymmetric saddle.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up v6 source, CAD, exports, reports, plan, and screenshots. | yes | 2026-08-27 |
| TASK-002 | Parameterize front/rear overhang, platform length/center, COG, and left cable allowance. | yes | 2026-08-27 |
| TASK-003 | Shorten the platform and side cheeks around the new tilt axis. | yes | 2026-08-27 |
| TASK-004 | Shift only the left cheek/trunnion/bearing/yoke outward by 20 mm. | yes | 2026-08-27 |
| TASK-005 | Widen the pan platform support to carry the asymmetric yoke span. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Validate operational clearances.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-006 | Add open-LCD and HDMI cable envelope objects and nominal collision checks. | yes | 2026-08-27 |
| TASK-007 | Add exact front/rear overhang, COG alignment, and side-clearance validation. | yes | 2026-08-27 |
| TASK-008 | Rebuild FCStd, STEP, standalone printable exports, and reports. | yes | 2026-08-27 |
| TASK-009 | Render and inspect v7 platform, HDMI/LCD, assembly, and comparison views. | yes | 2026-08-27 |
| TASK-010 | Update README, BOM, CAD checks, and mark this plan complete. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: Symmetric widening was rejected because it would provide only 10 mm on the side that needs a 20 mm cable allowance.
- **ALT-002**: Keeping the 160 mm plate was rejected because the requested front and rear camera overhangs intentionally eliminate unnecessary plastic.
- **ALT-003**: Leaving the tilt axis at the geometric camera center was rejected because the supplied center-of-mass estimate places it 10.3 mm forward of camera center.

## 4. Dependencies

- **DEP-001**: Panasonic HC-V760 operating instructions for LCD and Micro HDMI component placement.
- **DEP-002**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-003**: `/home/user/Applications/FreeCAD-1.1.3.AppImage` for screenshots.
- **DEP-004**: Local FFmpeg for the reference comparison.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - v7 geometry and checks.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v7 render set.
- **FILE-003**: `/home/user/pantilt/geometry_validation.json` - machine-readable acceptance results.
- **FILE-004**: `/home/user/pantilt/pantilt_hc_v760_nema17_gt2.FCStd` - complete assembly.
- **FILE-005**: `/home/user/pantilt/tilt_cradle_integral_gt2_80T.stl` - revised short saddle.
- **FILE-006**: `/home/user/pantilt/left_pan_yoke_lcd_clearance.stl` - rear-routed LCD-clearance support.
- **FILE-007**: `/home/user/pantilt/pan_platform_wide_150mm.stl` - widened pan platform.

## 6. Testing

- **TEST-001**: Require generated front and rear overhangs to equal 40 and 60 mm within 0.01 mm.
- **TEST-002**: Require tilt-axis-to-estimated-COG X error to be at most 0.01 mm.
- **TEST-003**: Require at least 20 mm camera-to-left-cheek clearance and unchanged right-side pulley/yoke clearances.
- **TEST-004**: Require zero nominal solid intersection with the LCD and HDMI clearance envelopes.
- **TEST-005**: Require valid B-reps, one integral tilt solid, and zero selected pose interference at -60, 0, and +60 degrees.
- **TEST-006**: Require non-empty v7 screenshots and original-resolution inspection of the short platform and left-side clearance.

## 7. Risks & Assumptions

- **RISK-001**: The LCD and connector envelopes are conservative placeholders; exact hinge and cable geometry still require physical measurement.
- **RISK-002**: A 39 mm saddle concentrates camera mounting loads and needs adequate wall thickness, infill, and a washer/insert around the 1/4-20 slot.
- **RISK-003**: The wider asymmetric yoke increases pan inertia and overhang on the left side.
- **ASSUMPTION-001**: Camera forward is +X and camera-left is +Y.
- **ASSUMPTION-002**: The 20 mm requirement is clear distance from the camera body to the nearest printed cheek, not total assembly widening.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/plan/design-direct-tilt-motor-mount-v6.md`

`https://www.panasonic.com/content/dam/Panasonic/support_manual/camcorders/english/HC-VX870M_Operating_Instructions.pdf`
