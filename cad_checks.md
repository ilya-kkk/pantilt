# CAD Checks V8

## Architecture
- Three-leg base with the pan motor mounted above its fixed plate and the shaft pointing downward.
- Pan axial load path uses a 51107 / 8107 35x52x12 mm thrust bearing in two 1 mm locating seats.
- Pan radial location uses a press-fit 608 in the lower base and a 7.9 mm plastic journal integral to the pan platform.
- The square (152 mm) topped pan platform, both pan yokes, both gussets, journal, thrust hub, connector skirt, and real 120T GT2/2MR pulley form one printed solid.
- The pan platform top face is a square plate, not a disc; both yoke footprints (left yoke y=66..76, right yoke y=-66.5..-56.5, both x=-76..52) sit fully inside it, with both gussets integral.
- Tilt rotating structure is one printed solid: plate, cheeks, hubs, two short 7.9 mm trunnions, and integral 80T pulley.
- Right-side order from camera outward is 80T pulley, plastic bearing trunnion, and 608 bearing.
- There is no shaft or printed material crossing the camera volume along the central tilt-axis span.
- Two shoulder-seated 608 bearings remain fixed in the pan yoke.
- Tilt belt plane is inboard of the right yoke wall at Y=-45.8 mm.
- Tilt motor front face seats directly against the right yoke; there is no separate slide plate or standoff.
- The right yoke contains one vertical pilot racetrack and four M3 tensioning slots over 14.0 mm travel.
- Camera saddle is 39.0x98.0 mm, leaving 40.0 mm front and 60.0 mm rear overhang.
- Tilt axis X=10.3 mm follows the stated camera COG at 79.8 mm from the rear.
- Camera-left clearance to the rotating cheek is 21.5 mm; the left fixed support is routed behind the LCD sweep.

## Drive
- Pan pitch diameter: 76.39 mm, ratio 6.0:1.
- Pan profile topology: 600 arcs, 120 land segments, closed=True.
- Pan compensated outside diameter: 75.6864 mm with a 10.0 mm face.
- Tilt pitch diameter: 50.93 mm, ratio 4.0:1.
- Integral tilt pulley uses a closed GT2/2MR modified-curvilinear outline with 80 teeth and a 10.0 mm face.
- Tilt profile topology: 400 arcs, 80 land segments, closed=True.
- Tilt pitch diameter: 50.9296 mm.
- Nominal 2MR outside diameter: 50.4216 mm.
- Compensated outside diameter: 50.2216 mm.
- Starting FDM compensation: 0.10 mm radial and 0.10 mm tangential.
- The pan 120T pulley uses the same closed GT2/2MR modified-curvilinear construction as the production tilt pulley.
- Selected tilt motor: StepperOnline 17HS19-2004S1, pilot 22.0x2.0 mm, mounting square 31.0 mm.
- Pilot diametral slot clearance: 0.60 mm.
- Motor-face gap to yoke: 0.000 mm.
- Shaft engagement into the 20T pulley envelope: 8.30 mm.

## Balance
- Nominal camera COG offset from the tilt axis: 1.00 mm.
- Nominal camera-only gravity torque: 0.0059 N m.

## Interference checks
- tilt_right_yoke_vs_motor_body: 0.000000 mm3
- tilt_right_yoke_vs_motor_pilot: 0.000000 mm3
- tilt_right_yoke_vs_motor_pulley: 0.000000 mm3
- tilt_right_yoke_vs_motor_shaft: 0.000000 mm3
- tilt_right_yoke_vs_integral_cradle: 0.000000 mm3
- tilt_right_608_vs_integral_cradle: 0.000000 mm3
- tilt_left_608_vs_integral_cradle: 0.000000 mm3
- tilt_right_yoke_vs_belt: 0.000000 mm3
- pan_base_vs_motor_body: 0.000000 mm3
- pan_base_vs_motor_pilot: 0.000000 mm3
- pan_base_vs_motor_shaft: 0.000000 mm3
- pan_base_vs_motor_pulley: 0.000000 mm3
- pan_base_vs_belt: 0.000000 mm3
- pan_base_vs_integral_pan: 0.000000 mm3
- pan_motor_vs_integral_pan: 0.000000 mm3
- pan_608_vs_integral_journal: 0.000000 mm3
- pan_51107_lower_vs_integral_pan: 0.000000 mm3
- pan_51107_upper_vs_integral_pan: 0.000000 mm3
- camera_vs_tilt_motor_nominal: 0.000000 mm3
- integral_cradle_vs_tilt_motor_nominal: 0.000000 mm3
- open_lcd_vs_integral_cradle: 0.000000 mm3
- open_lcd_vs_left_yoke: 0.000000 mm3
- hdmi_clearance_vs_integral_cradle: 0.000000 mm3
- hdmi_clearance_vs_left_yoke: 0.000000 mm3

## Tilt pose checks
- Tilt -60 deg: 0.000000 mm3
- Tilt 0 deg: 0.000000 mm3
- Tilt 60 deg: 0.000000 mm3

## Result
- Valid B-reps: True
- Integral tilt Part::Feature count: 1
- Integral tilt solid count: 1
- Integral pan Part::Feature count: 1
- Integral pan solid count: 1
- 51107 seat clearance: 0.40 mm diametral
- Pan 608 pocket interference: 0.10 mm diametral
- Plastic journal-to-608 clearance: 0.10 mm diametral
- Pan motor shaft points down: True
- Through tilt shaft present: False
- Central cross-shaft material: 0.000000 mm3
- Pulley closer to camera than right bearing: True
- Pulley-to-bearing center margin: 20.20 mm
- Pulley-to-right-yoke clearance: 1.60 mm
- Pulley-to-camera clearance: 7.20 mm
- Direct-mount slot count: 5
- Separate slide/standoff features: 0
- Geometry validation passed: True

## Production limitations
- Print and test the 2MR profile against the actual 10 mm belt, then tune the two explicit compensation parameters for the printer, material, nozzle, and slicer.
- Prototype the printed trunnion fit and check wear, creep, and layer orientation at both 608 bearings.
- Verify the actual 17HS19-2004S1 pilot height, shaft tolerances, pulley hub position, and connector clearance before printing the final yoke.
- Confirm the physical 51107 stack height, 608 fit, and closed-loop belt length before final printing.
- The central cable passage is intentionally removed because the integral plastic pan journal occupies the rotation axis; route cables outside the axis or add a later slip-ring solution.
- Add positive axial retention for transport or inverted operation; the present 51107 stack is retained downward by payload gravity.
- Measure the physical HC-V760 including battery, LCD travel, lens, and connectors.
- Verify the modeled LCD hinge X=35.0 mm and the HDMI plug envelope against the physical camera before final printing.
- Add final screw threads, inserts, tolerances, fillets, and print-orientation details.
