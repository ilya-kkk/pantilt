# Pan/Tilt CAD Assembly V2

This workspace generates a reference-like pan/tilt concept for a Panasonic HC-V760 payload.

## Architecture

- Three-leg printed base with the pan NEMA17 packaged below the turntable
- Sealed 110x86x12 mm pan turntable bearing with a 55 mm cable passage
- GT2 pan drive: 20T motor pulley and 120T driven ring, 6:1 ratio
- Compact two-sided yoke with local gussets and bearing bosses
- Two shoulder-seated 608 bearings and one continuous 8 mm steel tilt axle
- GT2 tilt drive fully outside the right yoke wall: 20T to 80T, 4:1 ratio
- External tilt motor slide with vertical belt-tension adjustment
- 160x78 mm camera plate with a longitudinal 1/4-20 mounting slot
- Nominal camera center of gravity within 1 mm of the tilt axis

## Generate

Run ./generate_pantilt_freecad.sh to regenerate the model.

Run ./open_pantilt_freecad.sh to open it.

Run /home/user/Applications/FreeCAD-1.1.3.AppImage make_screenshots_freecad.py to render the screenshot set.

## Outputs

- pantilt_hc_v760_nema17_gt2.FCStd
- pantilt_hc_v760_nema17_gt2.step
- geometry_validation.json
- cad_checks.md
- BOM.md
- screenshots/01_isometric_v2.png through screenshots/10_pan45_tilt18_v2.png
- screenshots/11_reference_comparison.png

## Verified Concept Checks

- Every generated B-rep is valid.
- The tilt belt, both pulleys, motor slide, and standoffs have zero solid interference with the right yoke.
- The pan belt has zero interference with the bearing adapter.
- The camera and cradle have zero measured interference at tilt angles -60, 0, and +60 degrees.
- The final screenshot set was rendered at 1600x1200 and visually compared with all three supplied reference photographs.

## Production Limitations

This is a mechanically coherent concept/fit model, not a print-ready release. Before manufacturing:

- replace visual GT2 teeth with exact vendor profiles;
- select and measure the actual turntable bearing and closed-loop belts;
- measure the HC-V760 with battery, open LCD, lens accessories, and connected cables;
- add exact screws, threaded inserts, bearing fits, fillets, print tolerances, and part splits;
- perform stiffness, vibration, motor-torque, and cable-fatigue checks.

The previous layout and screenshots are preserved under legacy_v1_20260827/.
