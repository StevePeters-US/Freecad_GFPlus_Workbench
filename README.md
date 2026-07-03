# Gridfinity+ Workbench for FreeCAD (GF+)

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=flat&logo=github-sponsors)](https://github.com/sponsors/StevePeters-US)
[![FreeCAD Compatibility](https://img.shields.io/badge/FreeCAD-1.0_RC2_/_0.21_/_0.20-blue.svg?logo=freecad&logoColor=white)](https://www.freecad.org/)
[![Printables Model](https://img.shields.io/badge/Printables-Model_765609-orange.svg?style=flat&logo=3d-printing)](https://www.printables.com/model/765609-gridfinity)
[![Thingiverse Model](https://img.shields.io/badge/Thingiverse-Model_6823865-2496ed.svg?logo=thingiverse&logoColor=white)](https://www.thingiverse.com/thing:6823865/comments#comment-7541438)
[![License](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](LICENSE)


## 📖 What is Gridfinity+ (GF+)?


 **Gridfinity+** is a snap-fit latching variant of the standard open-source Gridfinity ecosystem.

* **Secure Hold:** Bins lock physically into baseplates, preventing them from tipping over or sliding when drawers open and close.

* **Backward Compatible:** Gridfinity+ baseplates are designed to accept standard Gridfinity bins, preserving your existing prints.The baseplates also  feature slots which are designed to embed a short segment of common **1 x 15mm steel wire (I used a paperclip)**. This allows for traditional gridfintiy magnetic bins to function with GF+ baseplates.

---

## 🛠️ Workbench Features

The **Gridfinity+ Workbench** registers two main commands under the **Gridfinity+** menu and toolbar:

### 1. Create GF+ Baseplate
Generates a parametric baseplate using the `Gridfinity+Base_Template.FCStd` file.
* **Inputs:**
  * `NumX`: Number of grid columns (minimum: 1).
  * `NumY`: Number of grid rows (minimum: 1).
* **How it works:** The tool opens the template, updates the spreadsheet values `SizeX` and `SizeY`, triggers a parametric recompute, imports the resulting shape as a new body named `GFPlus_Baseplate_X_Y` in your active document, and sets its color to dark grey.

### 2. Create GF+ Bin
Generates modular bins with custom dimensions, heights, and physical tab placements.
* **Inputs:**
  * `NumX Range` (Min & Max): Allows batch generating bins of multiple column widths.
  * `NumY Range` (Min & Max): Allows batch generating bins of multiple row depths.
  * `Heights`: Comma-separated list of heights (e.g., `0.75, 1.25`, corresponding to the spreadsheet height variables `SizeZ`).
  * `Selection` (Tab Placement): Controls where the locking tabs are added to the bin:
    * `edges`: Tabs are only added along the outer edges of the overall bin.
    * `corners`: Tabs are only added on the outer corners of the overall bin.
    * `fill` (Max Tabs): Tabs are placed on all 4 faces of every grid unit in the bin.
    * `none`: Generates a standard flat-bottom bin without latching tabs.
* **How it works:** The tool automatically creates the base bin body, builds the connectors, positions the rotated latching/blank tabs according to your selection rules, and fuses them into a single solid body labeled `GFPlus_Bin_XxYxHeight_Selection` (colored in vibrant green).

## 🚀 Installation

### Option 1: Manual Link (Recommended for Development)
Simply link or copy this folder into your FreeCAD user directory so FreeCAD can load it at startup.

**Linux / macOS:**
```bash
ln -s /path/to/Freecad_GFPlus_Workbench ~/.local/share/FreeCAD/Mod/freecad.gridfinity_plus_workbench
```
*(On older versions of FreeCAD, the directory may be located at `~/.FreeCAD/Mod/`)*

**Windows (PowerShell):**
```powershell
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\FreeCAD\Mod\freecad.gridfinity_plus_workbench" -Value "C:\path\to\Freecad_GFPlus_Workbench"
```

### Option 2: Install via Python (Pip)
Since this workbench is packaged as a standard namespace package, you can install it using pip:
```bash
cd Freecad_GFPlus_Workbench
pip install .
```

## ⚖️ License

This project is licensed under **CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike). See the [LICENSE](LICENSE) file for details.
