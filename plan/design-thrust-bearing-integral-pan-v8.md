---
goal: Thrust Bearing Integral Pan V8
version: 8.0
date_created: 2026-08-28
last_updated: 2026-08-28
owner: Codex
status: Complete
tags: [freecad, mechanical, pan, gt2, bearing]
---

# Thrust Bearing Integral Pan V8

Replace the 110 mm turntable bearing and conceptual pan teeth with a low stack using a 51107 thrust bearing, a lower 608 radial bearing, an integral printed journal, and a real 120T GT2/2MR pulley.

## Requirements

- Seat a 51107/8107 35x52x12 mm bearing between 1 mm locating recesses in the fixed base and rotating pan platform.
- Press a 608-2RS into the fixed base and locate it with a 7.9 mm plastic journal integral to the rotating pan part.
- Combine the pan platform, thrust hub, journal, connector skirt, and 120T pulley into one printable solid.
- Use a production-profile 120T GT2/2MR pulley with a 10 mm face.
- Mount the pan NEMA17 above the fixed plate with its shaft pointing downward and retain 14 mm tension adjustment.
- Preserve all accepted v7 tilt, LCD, HDMI, and camera-saddle geometry.

## Verified Results

- 51107 seat: 52.4 mm diameter, 1.0 mm depth each side, 0.4 mm diametral clearance.
- Pan 608 pocket: 21.9 mm nominal diameter, 0.1 mm nominal diametral interference.
- Integral journal: 7.9 mm diameter, 0.1 mm diametral clearance to the 608 bore.
- Pan GT2 profile: 120 teeth, 600 arcs, 120 land segments, closed valid profile, 10 mm face.
- Pan and tilt printed mechanisms each contain one connected solid.
- Selected static and -60/0/+60 degree interference checks are zero.

## Production Notes

- Confirm press fits with small calibration coupons before printing full parts.
- Confirm the actual closed-loop pan belt after choosing the final motor position; 350 mm is the current estimate.
- Add positive axial retention for transport or inverted use.
- The integral central journal removes the previous central cable passage.

