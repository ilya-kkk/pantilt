---
goal: Inboard Integral Tilt Pulley V4
version: 4.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Completed'
tags: [design, architecture, freecad, mechanical, pan-tilt]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Reorder the right tilt support so the integral 80T pulley is closer to the camera than the right bearing journal. Preserve the one-piece printed tilt cradle and move only the right yoke support, bearing, motor-shaft passage, and tilt belt plane required by this order.

## 1. Requirements & Constraints

- **REQ-001**: Arrange the right tilt load path from the camera outward as cradle cheek, integral 80T pulley, plastic trunnion, and 608 bearing.
- **REQ-002**: Keep the camera plate, both cheeks, both hubs, both trunnions, and 80T pulley in exactly one `Part::Feature` containing one connected solid.
- **REQ-003**: Keep the 80T pulley center closer to camera centerline than the right 608 bearing center by at least 15 mm.
- **REQ-004**: Maintain at least 1 mm nominal lateral clearance between the 80T pulley flange and the right yoke bearing boss.
- **REQ-005**: Maintain at least 5 mm nominal lateral clearance between the camera envelope and the 80T pulley flange.
- **REQ-006**: Move the complete tilt belt path to the inboard side of the right yoke and align both pulley centers to that plane.
- **REQ-007**: Add a dedicated motor-shaft passage through the right yoke and require zero shaft-to-yoke interference.
- **REQ-008**: Preserve the left 608 support, no-through-shaft architecture, camera balance, and -60/0/+60 degree tilt range.
- **REQ-009**: Leave the pan bearing, pan drive ratio, pan motor, base, and central cable passage unchanged.
- **REQ-010**: Regenerate FCStd, STEP, validation, documentation, ten v4 views, and the comparison sheet.
- **CON-001**: Keep 10 mm nominal GT2 belt width and the existing 20T/80T tilt ratio.
- **CON-002**: Preserve v3 under `/home/user/pantilt/legacy_v3_outboard_pulley_20260827/`.
- **GUD-001**: Use the existing deterministic FreeCAD 1.1.3 Python generation workflow.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Reorder the right tilt support and drive plane.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up v3 source, model, STEP, reports, plan, and screenshots. | yes | 2026-08-27 |
| TASK-002 | Add explicit left/right yoke centers and move only the right yoke and 608 support outward. | yes | 2026-08-27 |
| TASK-003 | Move the integral 80T pulley to the camera side of the right bearing and shorten the bearing trunnion to start at the pulley. | yes | 2026-08-27 |
| TASK-004 | Move the motor pulley and belt plane inboard and add a right-yoke motor-shaft clearance hole. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Validate, render, and document v4.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-005 | Add machine-readable pulley-order and lateral-clearance checks and require them for validation success. | yes | 2026-08-27 |
| TASK-006 | Regenerate FCStd and STEP and require all B-reps and the integral tilt solid to remain valid. | yes | 2026-08-27 |
| TASK-007 | Require zero selected static interference and zero pose interference at -60, 0, and +60 degrees. | yes | 2026-08-27 |
| TASK-008 | Render and inspect all v4 views, with emphasis on the right-side sequence and belt plane. | yes | 2026-08-27 |
| TASK-009 | Generate the v4 reference comparison and update README, BOM, CAD checks, and this plan. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: Retaining the current right-yoke position was rejected because the 10 mm pulley and belt cannot fit between the camera cheek and bearing boss.
- **ALT-002**: Reducing the belt below 10 mm was rejected because it changes an accepted drive requirement and still leaves inadequate flange clearance.
- **ALT-003**: Moving the pulley into the camera envelope was rejected because it would violate payload clearance.

## 4. Dependencies

- **DEP-001**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-002**: `/home/user/Applications/FreeCAD-1.1.3.AppImage` for screenshot generation.
- **DEP-003**: Local FFmpeg for the v4 comparison sheet.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - v4 geometry and validation generator.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v4 rendering and comparison generator.
- **FILE-003**: `/home/user/pantilt/README.md` - current architecture and output documentation.
- **FILE-004**: `/home/user/pantilt/BOM.md` - generated concept bill of materials.
- **FILE-005**: `/home/user/pantilt/cad_checks.md` - generated dimensional and validation report.
- **FILE-006**: `/home/user/pantilt/geometry_validation.json` - machine-readable acceptance checks.

## 6. Testing

- **TEST-001**: Run `/home/user/pantilt/generate_pantilt_freecad.sh` and require exit code 0.
- **TEST-002**: Require the 80T pulley center absolute Y coordinate to be smaller than the right bearing center absolute Y coordinate by at least 15 mm.
- **TEST-003**: Require at least 1 mm pulley-to-yoke clearance and at least 5 mm pulley-to-camera clearance.
- **TEST-004**: Require the integral tilt feature count and solid count to equal one and the through-shaft flag to remain false.
- **TEST-005**: Require every selected intersection and every -60/0/+60 degree pose intersection to be at most 0.01 mm3.
- **TEST-006**: Require ten non-empty 1600x1200 v4 screenshots and one non-empty 1800x1200 comparison sheet, followed by original-resolution visual inspection.

## 7. Risks & Assumptions

- **RISK-001**: The longer motor shaft or shaft extension needed to reach the inboard pulley requires production-level bearing and coupling selection.
- **RISK-002**: Moving only the right support makes the yoke laterally asymmetric and may require stiffness optimization after physical testing.
- **RISK-003**: Printed trunnion wear, creep, and bearing fit remain prototype-dependent.
- **ASSUMPTION-001**: “Closer to the camera” means the 80T pulley is axially inboard of the right 608 bearing, not merely visually overlapping it.
- **ASSUMPTION-002**: The current pan mechanism remains provisionally accepted and outside the scope of v4.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/plan/design-integral-tilt-cradle-v3.md`

`/home/user/pantilt/legacy_v3_outboard_pulley_20260827/cad_checks.md`
