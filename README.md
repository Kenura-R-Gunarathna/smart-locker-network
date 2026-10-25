# Smart Locker Network

Pilot proposal and CAD models for the smart locker racks.

- `Smart Locker Network_ pilot proposal.html`: the pilot proposal
- `cad/rack.py`: CadQuery models of the slotted angle and the rack
- `cad/materials.md`: bill of materials and costs for one rack

## Setup

Install [pixi](https://pixi.sh) (`brew install pixi`), then from the project folder:

```sh
pixi install
```

This installs Python and CadQuery into `.pixi/`. Nothing is installed system-wide.

## Build the CAD files

```sh
pixi run build
```

This writes the models to `cad/out/` and prints the weights and costs. The folder is not committed, so run this after cloning or after changing `cad/rack.py`.

| File | What it is |
|---|---|
| `rack_7ft_3x1.5ft_6shelf_<gauge>.step` | Full rack with posts, shelves and bolts as separate parts |
| `rack_7ft_3x1.5ft_6shelf_<gauge>.stl` | Same rack as one mesh |
| `slotted_angle_38x38x<t>mm_<gauge>_10ft.step` | One 10 ft length of slotted angle |
| `slotted_angle_38x38x<t>mm_<gauge>_300mm.stl` | Short 300 mm sample of the angle |

`<gauge>` is 18G (1.2 mm), 16G (1.6 mm) or 14G (2.0 mm).

## Open the CAD files

### FreeCAD (recommended for STEP)

```sh
brew install --cask freecad
open -a FreeCAD "cad/out/rack_7ft_3x1.5ft_6shelf_16G.step"
```

In STEP files each post, shelf and set of bolts is a separate part, so you can hide parts, measure distances and cut sections. FreeCAD also opens STL files.

### VS Code live viewer (while editing `rack.py`)

1. Add the viewer to the environment: `pixi add ocp_vscode`
2. Install the **OCP CAD Viewer** extension in VS Code.
3. In `cad/rack.py`, add `from ocp_vscode import show` and call `show(assy)` on the rack you want to see.
4. Run `pixi run build`. The model appears in a VS Code panel and refreshes each time you run it.

### Without installing anything

- Drag a `.stl` file into an online viewer such as [viewstl.com](https://www.viewstl.com).
- On macOS, select a `.stl` file in Finder and press Space for Quick Look. Whether this works depends on your macOS version.
