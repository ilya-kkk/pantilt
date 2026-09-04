# CAD Checks V5

## Architecture
- Three-leg reference-like base with the pan motor below the turntable.
- Pan load path uses a 110x86x12 mm turntable bearing.
- Tilt rotating structure is one printed solid: plate, cheeks, hubs, two short 7.9 mm trunnions, and integral 80T pulley.
- Right-side order from camera outward is 80T pulley, plastic bearing trunnion, and 608 bearing.
- There is no shaft or printed material crossing the camera volume along the central tilt-axis span.
- Two shoulder-seated 608 bearings remain fixed in the pan yoke.
- Tilt belt plane is inboard of the right yoke wall at Y=-45.8 mm.
- Central pan cable passage is 55.0 mm.

## Drive
- Pan pitch diameter: 76.39 mm, ratio 6.0:1.
- Tilt pitch diameter: 50.93 mm, ratio 4.0:1.
- Integral tilt pulley uses a closed GT2/2MR modified-curvilinear outline with 80 teeth and a 10.0 mm face.
- Tilt profile topology: 400 arcs, 80 land segments, closed=True.
- Tilt pitch diameter: 50.9296 mm.
- Nominal 2MR outside diameter: 50.4216 mm.
- Compensated outside diameter: 50.2216 mm.
- Starting FDM compensation: 0.10 mm radial and 0.10 mm tangential.
- The pan 120T tooth representation remains conceptual and is outside this v5 change.
- Motor slots follow each belt tension direction.

## Balance
- Nominal camera COG offset from the tilt axis: 1.00 mm.
- Nominal camera-only gravity torque: 0.0059 N m.

## Interference checks
- tilt_right_yoke_vs_motor_pulley: 0.000000 mm3
- tilt_right_yoke_vs_motor_shaft: 0.000000 mm3
- tilt_right_yoke_vs_integral_cradle: 0.000000 mm3
- tilt_right_608_vs_integral_cradle: 0.000000 mm3
- tilt_left_608_vs_integral_cradle: 0.000000 mm3
- tilt_right_yoke_vs_belt: 0.000000 mm3
- tilt_standoffs_vs_belt: 0.000000 mm3
- tilt_slide_vs_belt: 0.000000 mm3
- pan_tower_vs_motor: 0.000000 mm3
- pan_adapter_vs_belt: 0.000000 mm3
- camera_vs_tilt_motor_nominal: 0.000000 mm3
- integral_cradle_vs_tilt_motor_nominal: 0.000000 mm3

## Tilt pose checks
- Tilt -60 deg: 0.000000 mm3
- Tilt 0 deg: 0.000000 mm3
- Tilt 60 deg: 0.000000 mm3

## Result
- Valid B-reps: True
- Integral tilt Part::Feature count: 1
- Integral tilt solid count: 1
- Through tilt shaft present: False
- Central cross-shaft material: 0.000000 mm3
- Pulley closer to camera than right bearing: True
- Pulley-to-bearing center margin: 20.20 mm
- Pulley-to-right-yoke clearance: 1.60 mm
- Pulley-to-camera clearance: 7.20 mm
- Geometry validation passed: True

## Production limitations
- Print and test the 2MR profile against the actual 10 mm belt, then tune the two explicit compensation parameters for the printer, material, nozzle, and slicer.
- Prototype the printed trunnion fit and check wear, creep, and layer orientation at both 608 bearings.
- Select a supported long-shaft tilt motor or shaft extension and verify runout at the inboard 20T pulley.
- Confirm the selected turntable bearing and closed-loop belt dimensions.
- Measure the physical HC-V760 including battery, LCD travel, lens, and connectors.
- Add final screw threads, inserts, tolerances, fillets, and print-orientation details.
