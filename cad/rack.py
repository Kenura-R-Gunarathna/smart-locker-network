"""Slotted angle and single-bay slotted angle rack, sized to what Sri Lankan
hardware shops stock: 1 1/2" x 1 1/2" (38 mm) angle in 14G/16G/18G,
10 ft lengths, 3 ft x 1 1/2 ft shelf plates, 5/16" (M8) nuts and bolts.

Run:  pixi run build
"""

from pathlib import Path

import cadquery as cq

INCH = 25.4
FT = 12 * INCH
STEEL_DENSITY = 7.85e-6  # kg/mm^3

# Gauge -> thickness (mm), with the per-metre prices you were quoted (LKR)
GAUGES = {
    "18G": {"t": 1.2, "lkr_per_m": (328, 377)},
    "16G": {"t": 1.6, "lkr_per_m": (426, 459)},
    "14G": {"t": 2.0, "lkr_per_m": (541, 574)},
}

LEG = 1.5 * INCH        # 38.1 mm flange
PITCH = 1 * INCH        # hole pitch along the angle
HOLE_D = 8.5            # round hole, fits 5/16" (M8) bolt
SLOT_LEN = 20.0         # elongated slot, alternating with round holes
STOCK_LENGTH = 10 * FT  # angles are sold in 10 ft lengths


def hole_centre(t):
    """Distance from the heel's outer face to the hole row on each flange."""
    return t + (LEG - t) / 2


def hole_zs(length):
    """Centres of the holes along the angle; even index = round, odd = slot."""
    n = int((length - PITCH / 2) // PITCH) + 1
    return [PITCH / 2 + i * PITCH for i in range(n) if PITCH / 2 + i * PITCH < length]


def slotted_angle(length, t):
    """L angle with its heel on the Z axis and flanges along +X and +Y."""
    angle = (
        cq.Workplane("XY")
        .polyline([(0, 0), (LEG, 0), (LEG, t), (t, t), (t, LEG), (0, LEG)])
        .close()
        .extrude(length)
    )
    c = hole_centre(t)
    zs = hole_zs(length)
    rounds = [z for i, z in enumerate(zs) if i % 2 == 0]
    slots = [z for i, z in enumerate(zs) if i % 2 == 1 and z + SLOT_LEN / 2 < length]

    # Flange along X (normal Y): XZ plane, local (x, y) = global (X, Z)
    # Flange along Y (normal X): YZ plane, local (x, y) = global (Y, Z)
    for plane in ("XZ", "YZ"):
        cutter = (
            cq.Workplane(plane).pushPoints([(c, z) for z in rounds]).circle(HOLE_D / 2).extrude(LEG, both=True)
            .union(
                cq.Workplane(plane).pushPoints([(c, z) for z in slots])
                .slot2D(SLOT_LEN, HOLE_D, 90).extrude(LEG, both=True)
            )
        )
        angle = angle.cut(cutter)
    return angle


def shelf(width, depth, plate_t=1.0, lip=1.25 * INCH):
    """Shelf plate with lips bent down on all four sides, top face at z=0."""
    outer = cq.Workplane("XY").box(width, depth, lip, centered=(False, False, False))
    inner = (
        cq.Workplane("XY")
        .box(width - 2 * plate_t, depth - 2 * plate_t, lip, centered=(False, False, False))
        .translate((plate_t, plate_t, -plate_t))
    )
    return outer.cut(inner).translate((0, 0, -lip))


def bolt(t):
    """5/16" hex bolt + nut, axis along -Y, head on the outside of a flange at y=0."""
    head = cq.Workplane("XZ").polygon(6, 13 / 0.866).extrude(5.5)  # XZ normal is -Y
    shank = cq.Workplane("XZ").circle(4).extrude(-(t + 1.0 + 8))
    nut = cq.Workplane("XZ").polygon(6, 13 / 0.866).extrude(-6.5).translate((0, t + 1.0, 0))
    return head.union(shank).union(nut)


def rack(
    t=1.6,
    height=7 * FT,
    width=3 * FT,
    depth=1.5 * FT,
    n_shelves=6,
    bottom=4 * INCH,
    top_gap=2 * INCH,
    plate_t=1.0,
):
    """One rack bay: 4 corner posts with the shelves sitting inside the angles.

    Shelf heights are snapped so the bolts land on round holes.
    """
    lip = 1.25 * INCH
    sw, sd = width - 2 * t, depth - 2 * t
    c = hole_centre(t)

    # Bolt height = shelf top - lip/2, and must be a round-hole centre (even index)
    round_zs = hole_zs(height)[::2]
    lo, hi = bottom - lip / 2, height - top_gap - lip / 2
    targets = [lo + i * (hi - lo) / (n_shelves - 1) for i in range(n_shelves)]
    bolt_zs = [min(round_zs, key=lambda z: abs(z - tz)) for tz in targets]
    shelf_tops = [z + lip / 2 for z in bolt_zs]

    post = slotted_angle(height, t)
    b = bolt(t)
    bolts = cq.Workplane("XY")
    for z in bolt_zs:
        # one bolt through each flange of the post
        bolts = bolts.union(b.translate((c, 0, z)))
        bolts = bolts.union(b.rotate((0, 0, 0), (0, 0, 1), -90).mirror("YZ").translate((0, c, z)))

    assy = cq.Assembly(name="slotted_angle_rack")
    grey = cq.Color(0.32, 0.34, 0.36)
    zinc = cq.Color(0.75, 0.75, 0.72)
    corners = [((0, 0), 0), ((width, 0), 90), ((width, depth), 180), ((0, depth), 270)]
    for i, ((x, y), rot) in enumerate(corners):
        loc = cq.Location(cq.Vector(x, y, 0), cq.Vector(0, 0, 1), rot)
        assy.add(post, name=f"post_{i + 1}", loc=loc, color=grey)
        assy.add(bolts, name=f"bolts_{i + 1}", loc=loc, color=zinc)
    tray = shelf(sw, sd, plate_t, lip)
    for i, z in enumerate(shelf_tops):
        assy.add(tray, name=f"shelf_{i + 1}", loc=cq.Location(cq.Vector(t, t, z)), color=grey)

    info = {
        "t": t,
        "height": height,
        "width": width,
        "depth": depth,
        "shelf_size": (sw, sd),
        "shelf_tops": shelf_tops,
        "n_shelves": n_shelves,
        "bolts": n_shelves * 8,
        "post_mass": post.val().Volume() * STEEL_DENSITY,
        "shelf_mass": tray.val().Volume() * STEEL_DENSITY,
    }
    return assy, info


def build(out_dir=Path(__file__).parent / "out"):
    out_dir.mkdir(exist_ok=True)

    # 1. One 10 ft stock length of each gauge, plus a 300 mm sample for viewing
    print("Slotted angle 1 1/2\" x 1 1/2\" (38.1 mm), 10 ft (3048 mm) stock length")
    print(f"{'gauge':6}{'t mm':>6}{'kg/m':>8}{'kg/length':>11}{'LKR/m':>14}{'LKR/length':>16}")
    for g, spec in GAUGES.items():
        full = slotted_angle(STOCK_LENGTH, spec["t"])
        sample = slotted_angle(300, spec["t"])
        name = f"slotted_angle_38x38x{spec['t']}mm_{g}"
        cq.exporters.export(full, str(out_dir / f"{name}_10ft.step"))
        cq.exporters.export(sample, str(out_dir / f"{name}_300mm.stl"))
        kg = full.val().Volume() * STEEL_DENSITY
        lo, hi = spec["lkr_per_m"]
        m = STOCK_LENGTH / 1000
        print(f"{g:6}{spec['t']:>6}{kg / m:>8.2f}{kg:>11.2f}{f'{lo}-{hi}':>14}{f'{lo * m:,.0f}-{hi * m:,.0f}':>16}")

    # 2. One rack, built in every gauge so they can be compared
    print("\nRack: 7 ft tall, 3 ft x 1.5 ft shelves, 6 shelves, 1 mm shelf plate")
    for g, spec in GAUGES.items():
        assy, info = rack(t=spec["t"])
        name = f"rack_7ft_3x1.5ft_6shelf_{g}"
        assy.export(str(out_dir / f"{name}.step"))
        assy.export(str(out_dir / f"{name}.stl"))
        posts_m = 4 * info["height"] / 1000
        lo, hi = spec["lkr_per_m"]
        print(
            f"  {g}: posts 4 x {info['height']:.0f} mm = {posts_m:.2f} m angle "
            f"(4 x 10 ft lengths if cut one post per length), "
            f"posts {4 * info['post_mass']:.1f} kg, shelves {info['n_shelves'] * info['shelf_mass']:.1f} kg, "
            f"angle cost LKR {lo * posts_m:,.0f}-{hi * posts_m:,.0f} "
            f"(LKR {lo * 4 * STOCK_LENGTH / 1000:,.0f}-{hi * 4 * STOCK_LENGTH / 1000:,.0f} for 4 full lengths)"
        )
    print(f"  Shelf plate {info['shelf_size'][0]:.0f} x {info['shelf_size'][1]:.0f} mm, "
          f"tops at {', '.join(f'{z:.0f}' for z in info['shelf_tops'])} mm")
    print(f"  Nuts and bolts: {info['bolts']} x 5/16\" (M8) x 5/8\"")
    print(f"\nFiles in {out_dir}")


if __name__ == "__main__":
    build()
