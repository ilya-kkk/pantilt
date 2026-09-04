# Pan/Tilt CAD Assembly V7

This workspace generates a reference-like pan/tilt concept for a Panasonic HC-V760 payload.

## Architecture

- Three-leg printed base with the pan NEMA17 packaged below the turntable
- Sealed 110x86x12 mm pan turntable bearing with a 55 mm cable passage
- GT2 pan drive: 20T motor pulley and 120T driven ring, 6:1 ratio
- Asymmetric two-sided yoke with a rear-routed left bearing support that clears the open LCD through the tilt sweep
- Two shoulder-seated 608 bearings fixed in the pan yoke
- One printed tilt solid combining the camera plate, both cheeks, two short 7.9 mm bearing trunnions, and the inboard 80T driven pulley
- Functional 2 mm pitch GT2/2MR modified-curvilinear profile on the integral tilt pulley: 80 teeth, 10 mm face, 50.9296 mm pitch diameter
- Explicit starting FDM fit compensation: 0.10 mm radial and 0.10 mm tangential, editable in `build_pantilt_freecad.py` and the model parameter sheet
- No shaft crosses the camera volume; each trunnion ends at its local cradle cheek
- Right-side order from camera outward: integral 80T pulley, plastic trunnion, then 608 bearing
- GT2 tilt drive inside the right yoke wall: 20T motor pulley to integral 80T cradle pulley, 4:1 ratio
- StepperOnline 17HS19-2004S1 tilt motor seated directly against the outside face of the right pan yoke
- Integrated NEMA17 interface in the yoke: 22.6 mm pilot racetrack and four M3 slots on a 31 mm square, all providing 14 mm vertical tension travel
- Stock 5x24 mm motor shaft passes through the yoke and engages the inboard 20T pulley; no extension, plate, or standoffs
- 39x98 mm camera saddle with a longitudinal 1/4-20 mounting slot
- 40 mm front overhang, 60 mm rear overhang, and 20 mm added camera-left HDMI clearance
- Tilt axis aligned to the stated COG 79.8 mm from the camera rear

## Generate

Run ./generate_pantilt_freecad.sh to regenerate the model.

Run ./open_pantilt_freecad.sh to open it.

Run /home/user/Applications/FreeCAD-1.1.3.AppImage make_screenshots_freecad.py to render the screenshot set and reference comparison sheet.

## Outputs

- pantilt_hc_v760_nema17_gt2.FCStd
- pantilt_hc_v760_nema17_gt2.step
- tilt_cradle_integral_gt2_80T.step
- tilt_cradle_integral_gt2_80T.stl
- right_pan_yoke_direct_nema17.step
- right_pan_yoke_direct_nema17.stl
- left_pan_yoke_lcd_clearance.step
- left_pan_yoke_lcd_clearance.stl
- pan_platform_wide_150mm.step
- pan_platform_wide_150mm.stl
- geometry_validation.json
- cad_checks.md
- BOM.md
- screenshots/01_isometric_v7.png through screenshots/10_pan45_tilt18_v7.png
- screenshots/11_reference_comparison_v7.png
- screenshots/12_gt2_2mr_profile_closeup_v7.png
- screenshots/13_direct_tilt_motor_mount_v7.png
- screenshots/14_integrated_nema17_tension_slots_v7.png
- screenshots/15_short_camera_saddle_v7.png
- screenshots/16_open_lcd_hdmi_clearance_v7.png

## Verified Concept Checks

- Every generated B-rep is valid.
- The complete printed tilt mechanism is exactly one `Part::Feature` containing exactly one connected solid.
- The tilt pulley profile is one closed valid face containing 400 circular arcs and 80 land segments, extruded to a 10 mm working width.
- The integral pulley has exactly 80 grooves at 2 mm pitch; its nominal outside diameter is 50.4216 mm and its compensated outside diameter is 50.2216 mm.
- The central 60 mm span of the tilt axis contains zero cradle material and no through-shaft object exists.
- The integral 80T pulley is at least 15 mm closer to the camera centerline than the right 608 bearing center.
- The pulley maintains at least 1 mm to the right yoke and 5 mm to the camera envelope.
- The separate tilt motor plate and standoffs are absent; the motor front face has zero gap to the right yoke.
- The central pilot opening and four M3 slots are cut directly into the yoke and provide 14 mm vertical travel.
- The 22 mm motor pilot has 0.6 mm diametral clearance and the stock 24 mm shaft engages the 20T pulley envelope by 8.3 mm.
- The tilt belt, motor body, pilot, shaft, and both pulleys have zero solid interference with the right yoke.
- The pan belt has zero interference with the bearing adapter.
- The camera and cradle have zero measured interference at tilt angles -60, 0, and +60 degrees.
- The open-LCD and 20 mm HDMI service envelopes have zero interference with the cradle and left yoke at -60, 0, and +60 degrees.
- The final screenshot set was rendered at 1600x1200 and visually compared with all three supplied reference photographs.

## Production Limitations

The integral tilt pulley is now printable working geometry rather than a visual tooth placeholder. Its profile follows the GT2 construction used by the FreeCAD TimingGear macro and the Gates 2MR pitch/dimensional convention. Before committing to the full cradle print:

- print a short fit test or a reduced prototype using the actual belt and tune `gt2_radial_print_clearance` and `gt2_tangential_print_clearance` for the printer, material, nozzle, and slicer;
- do not treat the pan 120T ring as production-ready: its teeth remain a conceptual visual representation in v7;
- verify the real motor pilot height, pulley hub position, connector orientation, and access for the four M3 screw heads;
- select and measure the actual turntable bearing and closed-loop belts;
- measure the HC-V760 with battery, open LCD, lens accessories, and connected cables;
- add exact screws, threaded inserts, bearing fits, fillets, print tolerances, and part splits;
- prototype the plastic trunnion-to-608 fit and evaluate journal wear, creep, and print-layer orientation;
- perform stiffness, vibration, motor-torque, and cable-fatigue checks.

Profile references:

- https://www.gates.com/content/dam/documents-library/catalogs/power-transmission-catalog.pdf
- https://reqrefusion.github.io/FreeCAD-Documentation-html/wiki/Macro_TimingGear.html

The accepted direct-motor-mount v6 is preserved under `legacy_v6_direct_motor_20260827/`. Earlier revisions remain under their corresponding legacy directories.
