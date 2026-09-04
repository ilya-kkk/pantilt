# Pan/Tilt CAD Assembly

This workspace generates a FreeCAD assembly for a Panasonic HC-V760 pan/tilt camera mechanism:

- Panasonic HC-V760 camera envelope: `65 x 73 x 139 mm`
- Two NEMA17 motors
- GT2-10 belt drives on pan and tilt
- Bearing-supported rotating axes: pan stack plus 608-style tilt shaft bearings
- Editable dimensions in `build_pantilt_freecad.py`

Generate with:

```bash
./generate_pantilt_freecad.sh
```

Open in FreeCAD:

```bash
./open_pantilt_freecad.sh
```

Expected outputs:

- `pantilt_hc_v760_nema17_gt2.FCStd`
- `pantilt_hc_v760_nema17_gt2.step`

The model is a layout/fit assembly, not a finalized printable part set. Measure the real camera with battery, lens cap, screen clearance, and cable exits before manufacturing.
