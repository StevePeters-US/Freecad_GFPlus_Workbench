# INDEX.md — Gridfinity+ Workbench

Single source of truth for agents navigating this codebase.  
**Update this file whenever you add, rename, or delete a file, class, or skill.**  
See `.agents/skills/update_index/SKILL.md` for update rules.

---

## File Map

| File | Role |
|------|------|
| `freecad/gridfinity_plus_workbench/init_gui.py` | Workbench entry point; registers commands and menus |
| `freecad/gridfinity_plus_workbench/CreateBin.py` | `CreateBin` command; tab placement, bin shape, connector, fusion |
| `freecad/gridfinity_plus_workbench/CreateBinTaskPanel.py` | Qt task panel for bin creation; batch range inputs |
| `freecad/gridfinity_plus_workbench/CreateBaseplate.py` | `CreateBaseplate` command; opens template, writes spreadsheet, extracts shape |
| `freecad/gridfinity_plus_workbench/CreateBaseplateTaskPanel.py` | Qt task panel for baseplate creation |
| `freecad/gridfinity_plus_workbench/__init__.py` | Package init |
| `freecad/gridfinity_plus_workbench/version.py` | Version string |

### Resource Files

| Path | Purpose |
|------|---------|
| `freecad/gridfinity_plus_workbench/resources/GF+BinTemplate.FCStd` | Parametric bin template; `Spreadsheet` has `SizeX`, `SizeY`, `SizeZ`; output feature: `Pad` |
| `freecad/gridfinity_plus_workbench/resources/GF+TabTemplate.FCStd` | Single tab shape; no spreadsheet |
| `freecad/gridfinity_plus_workbench/resources/GF+BlankTemplate.FCStd` | Blank tab placeholder |
| `freecad/gridfinity_plus_workbench/resources/GF+TabConnectorTemplate.FCStd` | Connector plate; `Spreadsheet` has `SizeX`, `SizeY`; output feature: `Pad005` |
| `freecad/gridfinity_plus_workbench/resources/Gridfinity+Base_Template.FCStd` | Parametric baseplate; `Spreadsheet` has `SizeX`, `SizeY`; output feature: `Cut001` |

---

## Class → File Index

| Class | File | Line |
|-------|------|------|
| `GridifintyPlusWorkbench` | `init_gui.py` | 16 |
| `CreateBin` | `CreateBin.py` | 9 |
| `CreateBaseplate` | `CreateBaseplate.py` | 6 |
| `BinTaskPanel` | `CreateBinTaskPanel.py` | 4 |
| `CommandCreateBin` | `CreateBinTaskPanel.py` | 115 |
| `BaseplateTaskPanel` | `CreateBaseplateTaskPanel.py` | — |

---

## Skill Dispatch Table

Load these skills when about to perform the indicated work:

| Skill | When to load |
|-------|-------------|
| `gfplus_freecad_env` | Before running any standalone Python or writing test scripts that import FreeCAD |
| `gfplus_logging` | Before adding any log, warning, or error output to any module |
| `gfplus_command_pattern` | Before adding a new command or task panel, or modifying an existing one |
| `gfplus_template_loading` | Before touching any code that opens, reads, or writes `.FCStd` template files |
| `gfplus_todo_format` | Before creating a new `todo_*.md` file or adding tasks to an existing one |
| `gfplus_code_review` | Before starting a code review session |
| `update_index` | Before adding, renaming, or deleting any file or class |

---

## Known Bugs

| ID | File:Line | Description | Fix hint |
|----|-----------|-------------|----------|
| B-001 | `CreateBin.py:130` | `connector_feature` None check uses `print()` not a proper log | Replace with `FreeCAD.Console.PrintWarning` |
| B-002 | `CreateBinTaskPanel.py:112` | Skip message uses `print()` | Replace with `FreeCAD.Console.PrintMessage` |
| B-003 | `CreateBaseplate.py:62` | Exception message uses `print()` | Replace with `FreeCAD.Console.PrintError` |

---

## Development Patterns

- All new commands must call `FreeCADGui.addCommand('CommandName', ClassName())` at module level.
- `IsActive()` should return `FreeCAD.ActiveDocument is not None` for commands that need a document.
- Tab placement uses 42 mm grid spacing; the center offset is `(-20.75, 0, 0)`.
- Object name scheme: `GFPlus_Bin_{NumX}x{NumY}x{Height:.2f}_{Selection}` (dots → underscores), `GFPlus_Baseplate_{NumX}_{NumY}`.
- Temporary intermediate objects are prefixed `ImportedTab_`, `ImportedBin`, `ImportedBaseplate` and are cleaned up after fusion/copy.
