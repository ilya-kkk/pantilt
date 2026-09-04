---
goal: Reference-Like Pan/Tilt Mechanical Architecture V2
version: 2.0
date_created: 2026-08-27
last_updated: 2026-08-27
owner: Codex
status: 'Completed'
tags: [design, architecture, freecad, mechanical, pan-tilt]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Replace the non-assemblable layout with a parameterized FreeCAD concept that follows the reference mechanism: a three-leg compact base, a low pan motor, a ring-supported turntable, a compact yoke, and an external tilt belt plane.

## 1. Requirements & Constraints

- **REQ-001**: Generate `/home/user/pantilt/pantilt_hc_v760_nema17_gt2.FCStd` and `/home/user/pantilt/pantilt_hc_v760_nema17_gt2.step` from `/home/user/pantilt/build_pantilt_freecad.py`.
- **REQ-002**: Use a three-leg printed base and package the pan NEMA17 below the rotating platform.
- **REQ-003**: Support pan with a purchased 110x86x12 mm turntable bearing and keep a central cable passage at least 55 mm in diameter.
- **REQ-004**: Use a 120T/20T GT2 pan reduction and an 80T/20T GT2 tilt reduction with exact visual tooth counts.
- **REQ-005**: Place the complete tilt belt path outside the right yoke wall with at least 2 mm nominal lateral clearance.
- **REQ-006**: Support tilt on two shoulder-seated 608 bearings, a continuous 8 mm steel axle, and external retaining caps/collars.
- **REQ-007**: Balance the Panasonic HC-V760 placeholder so its nominal center of gravity is within 2 mm of the tilt axis.
- **REQ-008**: Provide a longitudinal 1/4-20 camera slot and retain the 65x73x139 mm camera envelope.
- **REQ-009**: Generate normal, exploded, drive-focus, and tilt-pose screenshots plus a comparison sheet using the three supplied reference photos.
- **REQ-010**: Verify zero solid intersections for the selected belt, pulley, wall, motor, camera, and motion-pose clearance pairs.
- **CON-001**: Treat the result as a concept/fit model; exact vendor bearing geometry, GT2 tooth profile, camera ports, fasteners, and print tolerances require production detailing.
- **CON-002**: Preserve the previous generator and artifacts under `/home/user/pantilt/legacy_v1_20260827/`.
- **GUD-001**: Use the existing FreeCAD 1.1.3 AppImage runtime and Python-based deterministic generation workflow.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Replace the mechanical architecture and generation code.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Back up the v1 generator, model, STEP, reports, and screenshots to `/home/user/pantilt/legacy_v1_20260827/`. | yes | 2026-08-27 |
| TASK-002 | Rewrite `/home/user/pantilt/build_pantilt_freecad.py` with three named subassemblies: fixed base, pan rotating, and tilt rotating. | yes | 2026-08-27 |
| TASK-003 | Implement the pan turntable bearing, 120T drive ring, low motor mount, three-leg base, and cable passage. | yes | 2026-08-27 |
| TASK-004 | Implement the compact yoke, shoulder-seated 608 bearings, continuous axle, external 80T tilt drive, and balanced camera cradle. | yes | 2026-08-27 |

### Implementation Phase 2

- GOAL-002: Validate, render, and compare the v2 concept.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-005 | Regenerate FCStd and STEP and verify all generated B-reps are valid. | yes | 2026-08-27 |
| TASK-006 | Generate `/home/user/pantilt/geometry_validation.json` and require every listed interference volume to be at most 0.01 mm3. | yes | 2026-08-27 |
| TASK-007 | Rewrite `/home/user/pantilt/make_screenshots_freecad.py` and render assembly, exploded, focus, and +/-60 degree tilt poses. | yes | 2026-08-27 |
| TASK-008 | Create `/home/user/pantilt/screenshots/11_reference_comparison.png` from the v2 render and supplied reference photographs. | yes | 2026-08-27 |
| TASK-009 | Inspect all output images at original resolution and iterate until the architecture is visually consistent with the reference. | yes | 2026-08-27 |

## 3. Alternatives

- **ALT-001**: A single 35x52x12 thrust bearing was rejected because it does not provide a complete radial and overturning-moment load path.
- **ALT-002**: Two vertically separated 608 pan bearings were rejected because they eliminate the large central cable passage and resemble the reference less closely.
- **ALT-003**: An idler-based tilt tensioner was rejected for this concept because vertical motor slots provide a simpler and fully modeled belt-tension adjustment.

## 4. Dependencies

- **DEP-001**: `/home/user/pantilt/squashfs-root/usr/bin/freecadcmd` from FreeCAD 1.1.3.
- **DEP-002**: FreeCAD GUI runtime available through `/home/user/Applications/FreeCAD-1.1.3.AppImage` for screenshot generation.
- **DEP-003**: ImageMagick or an equivalent local image compositor for the comparison sheet.

## 5. Files

- **FILE-001**: `/home/user/pantilt/build_pantilt_freecad.py` - authoritative v2 geometry generator.
- **FILE-002**: `/home/user/pantilt/make_screenshots_freecad.py` - v2 rendering and motion-pose generator.
- **FILE-003**: `/home/user/pantilt/README.md` - architecture, generation, and limitation notes.
- **FILE-004**: `/home/user/pantilt/BOM.md` - generated v2 concept bill of materials.
- **FILE-005**: `/home/user/pantilt/cad_checks.md` - generated dimensions and validation summary.
- **FILE-006**: `/home/user/pantilt/geometry_validation.json` - machine-readable geometric checks.

## 6. Testing

- **TEST-001**: Run `/home/user/pantilt/generate_pantilt_freecad.sh` and require exit code 0.
- **TEST-002**: Open the generated FCStd headlessly and require every object with a `Shape` to report `Shape.isValid() == true`.
- **TEST-003**: Require zero interference between the right yoke and each tilt belt component.
- **TEST-004**: Require zero interference between the camera/cradle and fixed pan/yoke components at tilt angles -60, 0, and +60 degrees.
- **TEST-005**: Require every screenshot to be a non-empty 1600x1200 PNG and visually inspect the final comparison sheet.

## 7. Risks & Assumptions

- **RISK-001**: The reference photographs do not reveal the internal pan bearing type or exact dimensions; the turntable bearing is an explicit engineering inference.
- **RISK-002**: The camera placeholder omits exact HC-V760 battery, display hinge, connector, and lens geometry.
- **RISK-003**: Generated pulley teeth are visual approximations and must be replaced by a vendor profile before manufacturing.
- **ASSUMPTION-001**: Conceptual resemblance means matching packaging and load-path architecture rather than reproducing undocumented dimensions.
- **ASSUMPTION-002**: A 0.6 kg payload and non-continuous pan travel are acceptable for the concept.

## 8. Related Specifications / Further Reading

`/home/user/pantilt/README.md`

`/home/user/pantilt/legacy_v1_20260827/cad_checks.md`
