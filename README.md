# Pan/Tilt CAD Assembly V8

The printable V9 redesign is in [`v9/`](v9/): [FreeCAD assembly](v9/output/PanTilt_V9_HC-V760.FCStd), [printing and assembly guide](v9/README_RU.md), [STL parts](v9/output/stl/) and [bill of materials](v9/BOM_RU.md). V9 uses ordinary M3 screws with side-fed nuts and places the fixed pan motor below the rotating platform. The V8 reference and its history are documented below.

This workspace generates a reference-like pan/tilt concept for a Panasonic HC-V760 payload.

## Architecture

- Three-leg printed base with integral 51107 and 608 bearing seats
- Pan axial bearing: 51107/8107, 35x52x12 mm, seated 1 mm into both printed parts
- Pan radial bearing: press-fit 608-2RS in the lower base with an integral 7.9 mm plastic journal on the upper pan part
- Real GT2/2MR pan drive: downward-facing 20T motor pulley and integral printed 120T driven pulley, 10 mm face, 6:1 ratio
- Pan NEMA17 mounted above the fixed plate with its shaft pointing downward and 14 mm belt-tension travel
- One printable pan-rotating solid: 160 mm square-topped pan platform with the asymmetric two-sided yoke (rear-routed left bearing support that clears the open LCD through the tilt sweep; direct-NEMA17 right support), both gussets, plastic journal, thrust hub, skirt, and integral 120T pulley fused into a single connected solid — `PAN_ROTATING_one_piece_platform_journal_120T_GT2`
- Two shoulder-seated 608 bearings fixed in the pan yoke (the bearings and their caps stay separate insertable parts)
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
- pan_one_piece_square_platform_yokes_120T_GT2.step
- pan_one_piece_square_platform_yokes_120T_GT2.stl
- base_51107_608_downshaft_nema17.step
- base_51107_608_downshaft_nema17.stl
- geometry_validation.json
- cad_checks.md
- BOM.md
- screenshots/01_isometric_v8.png through screenshots/10_pan45_tilt18_v8.png
- screenshots/11_reference_comparison_v8.png through screenshots/19_pan_motor_shaft_down_v8.png

## Verified Concept Checks

- Every generated B-rep is valid.
- The complete printed tilt mechanism is exactly one `Part::Feature` containing exactly one connected solid.
- The complete pan rotating printed assembly — square-topped platform, both pan yokes, both gussets, plastic journal, thrust hub, connector skirt, and 120T pulley — is exactly one `Part::Feature` containing exactly one connected solid.
- The pan 120T profile contains 600 circular arcs and 120 land segments and is extruded to a 10 mm working width.
- The 51107 seat has 0.4 mm diametral clearance; the 608 pocket has 0.1 mm nominal diametral interference; the plastic journal has 0.1 mm diametral clearance in the 608 inner ring.
- The pan motor shaft points downward and its mounting face is flush with the fixed plate.
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
- print a short pan 120T tooth-sector fit test with the actual belt before committing to the full platform;
- verify the real motor pilot height, pulley hub position, connector orientation, and access for the four M3 screw heads;
- measure the actual 51107 stack, 608 bearings, and closed-loop belts;
- tune the nominal `21.9 mm` 608 press-fit pocket for the specific printer and material;
- add positive axial retention if the unit must survive transport shocks or inverted operation;
- the central cable passage is no longer available because the plastic pan journal occupies the axis;
- measure the HC-V760 with battery, open LCD, lens accessories, and connected cables;
- add exact screws, threaded inserts, bearing fits, fillets, print tolerances, and part splits;
- prototype the plastic trunnion-to-608 fit and evaluate journal wear, creep, and print-layer orientation;
- perform stiffness, vibration, motor-torque, and cable-fatigue checks.

Profile references:

- https://www.gates.com/content/dam/documents-library/catalogs/power-transmission-catalog.pdf
- https://reqrefusion.github.io/FreeCAD-Documentation-html/wiki/Macro_TimingGear.html

The accepted short-saddle v7 is preserved under `legacy_v7_short_hdmi_20260827/`. Earlier revisions remain under their corresponding legacy directories.
# pantilt
