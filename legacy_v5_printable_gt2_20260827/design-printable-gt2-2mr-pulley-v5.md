---
goal: Printable GT2 2MR Integral Tilt Pulley V5
version: 5.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Completed'
tags: [design, freecad, mechanical, gt2, fdm]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Replace the decorative rectangular teeth on the integral 80T tilt pulley with a continuous printable GT2/2MR groove profile. Preserve the accepted v4 architecture, expose FDM fit compensation, and export the complete one-piece tilt cradle as standalone STEP and STL files.

## 1. Requirements & Constraints

- **REQ-001**: Generate the 80T driven pulley from a closed 2 mm pitch modified-curvilinear GT2/2MR profile, not discrete rectangular boxes.
- **REQ-002**: Keep the pulley face width at 10 mm and the tilt ratio at 20T/80T = 4:1.
- **REQ-003**: Keep camera plate, cheeks, hubs, trunnions, and driven pulley in one `Part::Feature` containing one connected solid.
- **REQ-004**: Expose radial and tangential FDM compensation parameters without changing tooth count or pitch diameter.
- **REQ-005**: Validate profile closure, profile face validity, tooth count, pitch diameter, outside diameter, and generated arc count.
- **REQ-006**: Preserve the no-through-shaft architecture, inboard pulley order, bearing/yoke clearances, and -60/0/+60 degree collision-free tilt range.
- **REQ-007**: Export the full assembly plus standalone printable tilt-cradle STEP and STL artifacts.
- **REQ-008**: Render v5 assembly views, a pulley profile close-up, and a new reference comparison sheet.
- **CON-001**: Leave the provisional pan mechanism and its visual 120T tooth representation unchanged.
- **CON-002**: Preserve v4 under `/home/user/pantilt/legacy_v4_visual_gt2_20260827/`.
- **GUD-001**: Use the existing deterministic FreeCAD 1.1.3 Python workflow.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Build the functional 2MR geometry.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up the complete v4 source, model, reports, plan, and screenshots. | yes | 2026-08-27 |
| TASK-002 | Implement the 2MR groove outline from circular arcs and connecting land segments. | yes | 2026-08-27 |
| TASK-003 | Add explicit radial and tangential print-fit compensation parameters. | yes | 2026-08-27 |
| TASK-004 | Fuse the profiled 80T body and flanges into the existing one-piece tilt cradle. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Validate and deliver print artifacts.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-005 | Add profile topology and dimensional acceptance checks to `geometry_validation.json`. | yes | 2026-08-27 |
| TASK-006 | Export assembly FCStd/STEP and standalone tilt cradle STEP/STL. | yes | 2026-08-27 |
| TASK-007 | Re-run B-rep, one-solid, clearance, and tilt-pose interference checks. | yes | 2026-08-27 |
| TASK-008 | Render and visually inspect v5 views and the profile close-up. | yes | 2026-08-27 |
| TASK-009 | Update README, BOM, CAD checks, and mark this plan complete. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: Rectangular radial teeth were rejected because they do not mate with the modified-curvilinear GT2 belt tooth.
- **ALT-002**: Importing a vendor mesh was rejected because it would remove deterministic parametric control and complicate fusion into the cradle.
- **ALT-003**: Claiming a universal zero-clearance profile was rejected because FDM shrinkage, extrusion width, and actual belt tolerances require printer-specific calibration.

## 4. Dependencies

- **DEP-001**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-002**: `/home/user/Applications/FreeCAD-1.1.3.AppImage` for GUI screenshot rendering.
- **DEP-003**: Gates 2MR dimensions and the FreeCAD TimingGear GT2 arc construction.
- **DEP-004**: Local FFmpeg for the reference comparison sheet.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - v5 profile, assembly, validation, and export generator.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v5 rendering and comparison generator.
- **FILE-003**: `/home/user/pantilt/geometry_validation.json` - machine-readable profile and assembly checks.
- **FILE-004**: `/home/user/pantilt/tilt_cradle_integral_gt2_80T.step` - standalone editable tilt part.
- **FILE-005**: `/home/user/pantilt/tilt_cradle_integral_gt2_80T.stl` - standalone printable tilt part.
- **FILE-006**: `/home/user/pantilt/README.md` - manufacturing scope and calibration guidance.

## 6. Testing

- **TEST-001**: Run `/home/user/pantilt/generate_pantilt_freecad.sh` and require exit code 0.
- **TEST-002**: Require a closed, valid 80T profile with 400 circular arcs and 80 land segments.
- **TEST-003**: Require the integral tilt feature and solid counts to equal one and all generated B-reps to be valid.
- **TEST-004**: Require every selected static and -60/0/+60 degree pose intersection to be at most 0.01 mm3.
- **TEST-005**: Require standalone STEP/STL outputs to exist and the STL to contain a nonzero mesh.
- **TEST-006**: Require non-empty 1600x1200 v5 screenshots plus original-resolution visual inspection of the pulley close-up and reference comparison.

## 7. Risks & Assumptions

- **RISK-001**: The starting print compensation is geometrically explicit but must still be calibrated with the actual belt, material, nozzle, slicer, and printer.
- **RISK-002**: Fine 2 mm pitch features may print poorly with coarse nozzles or unfavorable part orientation.
- **RISK-003**: Printed trunnion wear, creep, and layer adhesion remain physical-test concerns.
- **ASSUMPTION-001**: The belt is a 2 mm pitch GT2/2MR-compatible belt with a nominal 10 mm width.
- **ASSUMPTION-002**: The user wants the integrated tilt pulley upgraded now; the pan ring remains provisional for later review.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/plan/design-inboard-tilt-pulley-v4.md`

`https://www.gates.com/content/dam/documents-library/catalogs/power-transmission-catalog.pdf`

`https://reqrefusion.github.io/FreeCAD-Documentation-html/wiki/Macro_TimingGear.html`
