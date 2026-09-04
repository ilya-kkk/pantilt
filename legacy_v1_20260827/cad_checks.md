# CAD Checks

## Load path
- Pan load path: camera -> tilt cradle -> tilt supports -> rotating upper plate -> pan hub bearings -> base.
- Tilt load path: camera -> camera plate -> 8 mm tilt axle -> two 608 bearings -> yoke supports.
- NEMA17 shafts are motor-input shafts only and do not support camera mass.

## Parameters
- Pan driven pitch diameter: 50.93 mm from 80T GT2.
- Tilt driven pitch diameter: 50.93 mm from 80T GT2.
- Bearing pocket clearance parameter: 0.15 mm.
- Tilt axis height above camera plate: 40.0 mm.

## Motion checks
- Pan check poses represented by reference axis: -90, 0, +90 deg. Center bearing stack is axisymmetric; motor is offset and belt plane clears top platform in nominal CAD.
- Tilt check poses considered by camera envelope and 95 mm inner yoke width: -60, 0, +60 deg are intended. Final collision must be rechecked after exact battery/cable geometry.

## Center of gravity
- CAMERA_COG is shown near the camera envelope center. Initial offset from TiltAxis is about dx=16.0 mm, dz=1.0 mm.
- Reduce this offset by sliding the camera in the 1/4-20 longitudinal slot and adjusting TILT_AXIS_HEIGHT_ABOVE_PLATE.
