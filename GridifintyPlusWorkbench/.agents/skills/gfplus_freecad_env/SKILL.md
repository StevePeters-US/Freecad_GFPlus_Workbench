---
name: GFPlus FreeCAD Environment
description: How FreeCAD is installed and how to import its Python modules when running agent scripts or standalone tests on Windows.
---

# GFPlus FreeCAD Environment

FreeCAD is installed as a standard Windows application. The workbench itself has no
automated test runner — all testing is done manually inside FreeCAD.

---

## Typical Install Paths (Windows)

```
C:\Program Files\FreeCAD 1.0\
C:\Users\<user>\AppData\Local\FreeCAD\
```

The bundled Python lives at `<install>\bin\python.exe` (Python 3.11).

---

## Workbench Installation

For development, symlink or copy this repo into FreeCAD's Mod directory:

```
%APPDATA%\FreeCAD\Mod\gridfinity_plus_workbench\
```

Then restart FreeCAD. The workbench appears in the workbench selector.

---

## Running Python Scripts That Import FreeCAD

FreeCAD modules are **not** importable from a plain Python installation.
To run a script that needs `import FreeCAD`, use FreeCAD's bundled Python:

```powershell
& "C:\Program Files\FreeCAD 1.0\bin\python.exe" your_script.py
```

Or add the FreeCAD lib directory to `PYTHONPATH` first:

```powershell
$env:PYTHONPATH = "C:\Program Files\FreeCAD 1.0\lib"
python your_script.py
```

---

## Stubbing FreeCAD for Pure-Logic Tests

For code that uses `FreeCAD.Vector` / `FreeCAD.Base.Placement` but no GUI, stub the module:

```python
import sys
from types import ModuleType

fc = ModuleType("FreeCAD")
class _Vec:
    def __init__(self, x=0, y=0, z=0): self.x = x; self.y = y; self.z = z
fc.Vector = _Vec
sys.modules["FreeCAD"] = fc
```

---

## Recommended Test Strategy

1. **Pure placement / geometry math** → stub FreeCAD (no install needed).
2. **Template loading / shape extraction** → requires a real FreeCAD install; test manually inside FreeCAD.
3. **GUI / task panels** → cannot be tested headlessly; verify visually in FreeCAD.
