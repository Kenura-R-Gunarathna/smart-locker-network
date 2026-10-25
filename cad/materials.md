# Materials: slotted angle rack (1 rack)

Model: `cad/rack.py`. Build it with `pixi run build`, and the files land in `cad/out/`.

## Rack size

| Item | Size |
|---|---|
| Height | 7 ft (2134 mm) |
| Width × depth | 3 ft × 1.5 ft (914 × 457 mm) |
| Shelves | 6 |
| Shelf tops (from floor) | 79, 486, 892, 1299, 1705, 2061 mm |

## Bill of materials

| # | Part | Spec | Qty | Notes |
|---|---|---|---|---|
| 1 | Slotted angle (posts) | 1½″ × 1½″ (38 mm), 16G (1.6 mm) recommended | 4 × 7 ft (8.53 m) | Sold in 10 ft lengths, so buy 4 lengths (3 ft offcut each) |
| 2 | Shelf plate | 3 ft × 1.5 ft, about 1 mm (20G) sheet, 1¼″ lips bent down on 4 sides | 6 | About 3.9 kg each, 23.4 kg total |
| 3 | Nut and bolt | 5/16″ (M8) × 5/8″, zinc plated | 48 (+ spares) | 8 per shelf, 2 at each corner |
| 4 | Foot plate / rubber shoe | To suit 38 mm angle | 4 | Optional, protects the floor |

Hole pattern on the angle: Ø8.5 mm round holes alternating with 8.5 × 20 mm slots at a 1″ (25.4 mm) pitch, on both flanges.

## Slotted angle by gauge

| Gauge | Thickness | Weight | LKR per metre | LKR per 10 ft length |
|---|---|---|---|---|
| 18G | 1.2 mm | 0.63 kg/m | 328–377 | 1,000–1,149 |
| 16G | 1.6 mm | 0.83 kg/m | 426–459 | 1,298–1,399 |
| 14G | 2.0 mm | 1.03 kg/m | 541–574 | 1,649–1,750 |

## Cost of the angle for one rack

| Gauge | Posts only (8.53 m) | 4 full 10 ft lengths |
|---|---|---|
| 18G | LKR 2,799–3,217 | LKR 3,999–4,596 |
| 16G | LKR 3,636–3,917 | LKR 5,194–5,596 |
| 14G | LKR 4,617–4,899 | LKR 6,596–6,998 |

Shelf plates and bolts are not priced yet. Get quotes for them from the same shop.

## Notes

- The 10 ft stock length is an assumption. Confirm it with the shop.
- A 1.5 ft deep shelf with about 40 cm between shelves does not fit the 25 × 60 × 60 cm lockers in the pilot proposal. For lockers, use `rack(depth=2 * FT, n_shelves=4)` in `cad/rack.py`. That gives 2 ft deep shelves about 66 cm apart, and a 3 ft shelf holds 3 lockers side by side. Check that 3 ft × 2 ft shelf plates are sold locally.
