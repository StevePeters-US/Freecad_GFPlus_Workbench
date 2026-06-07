---
name: GFPlus Logging
description: Logging conventions for the Gridfinity+ workbench. Required reading before adding any log output to any module.
---

# GFPlus Logging

All user-visible output goes through `FreeCAD.Console`. **Never use `print()`** — it only
appears in the terminal and not in the FreeCAD Report View.

---

## API

```python
FreeCAD.Console.PrintMessage("text\n")   # white — normal status
FreeCAD.Console.PrintWarning("text\n")   # yellow — non-fatal issue
FreeCAD.Console.PrintError("text\n")     # red — failure, always visible
FreeCAD.Console.PrintLog("text\n")       # grey — verbose; only shown when Log is enabled in Report View
```

All messages **must end with `\n`**.

---

## Prefix Convention

Always prefix messages with `[GFPlus]` and the calling class or method name so failures
are traceable:

```python
FreeCAD.Console.PrintError(f"[GFPlus] CreateBin.load_connector_shape: no feature Pad005\n")
FreeCAD.Console.PrintWarning(f"[GFPlus] BinTaskPanel.CreateBin: bin {name} already exists, skipping\n")
```

---

## Exception Logging

Catch and log with full context — never just the message:

```python
import traceback

try:
    doc = FreeCAD.open(path)
except Exception as e:
    FreeCAD.Console.PrintError(
        f"[GFPlus] CreateBaseplate._openBaseplateTemplate: {e}\n"
        f"{traceback.format_exc()}"
    )
    return None
```

---

## Rules

- No `print()` anywhere in production code.
- No empty `except: pass` blocks (see `.agents/rules/no_silent_exceptions.md`).
- Use `PrintLog` for verbose/debug output that the user does not normally need to see.
- Use `PrintWarning` for recoverable conditions (skipped objects, missing optional features).
- Use `PrintError` for failures that prevent the operation from completing.
