# CAD Checks V3

## Architecture
- Three-leg reference-like base with the pan motor below the turntable.
- Pan load path uses a 110x86x12 mm turntable bearing.
- Tilt rotating structure is one printed solid: plate, cheeks, hubs, two short 7.9 mm trunnions, and integral 80T pulley.
- There is no shaft or printed material crossing the camera volume along the central tilt-axis span.
- Two shoulder-seated 608 bearings remain fixed in the pan yoke.
- Tilt belt plane is fully outside the right yoke wall.
- Central pan cable passage is 55.0 mm.

## Drive
- Pan pitch diameter: 76.39 mm, ratio 6.0:1.
- Tilt pitch diameter: 50.93 mm, ratio 4.0:1.
- Visual pulley geometry contains exactly 120 pan teeth and 80 tilt teeth.
- Motor slots follow each belt tension direction.

## Balance
- Nominal camera COG offset from the tilt axis: 1.00 mm.
- Nominal camera-only gravity torque: 0.0059 N m.

## Interference checks
- tilt_right_yoke_vs_motor_pulley: 0.000000 mm3
- tilt_right_yoke_vs_integral_cradle: 0.000000 mm3
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
- Geometry validation passed: True

## Production limitations
- Replace visual pulley teeth with an exact vendor GT2 profile.
- Prototype the printed trunnion fit and check wear, creep, and layer orientation at both 608 bearings.
- Confirm the selected turntable bearing and closed-loop belt dimensions.
- Measure the physical HC-V760 including battery, LCD travel, lens, and connectors.
- Add final screw threads, inserts, tolerances, fillets, and print-orientation details.
