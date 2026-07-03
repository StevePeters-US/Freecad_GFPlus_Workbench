---
description: Ensure exceptions and logical failures are logged, not silently ignored.
---

# No Silent Exceptions

When writing `try...except` blocks or handling any logic operation that might fail, you
**MUST NOT** fail silently.

All exceptions or significant logical failures must be logged using FreeCAD's console:

```python
FreeCAD.Console.PrintError(f"[GFPlus] Error in MyMethod: {e}\n")
```

Do not use empty `except:` or `except Exception:` blocks with only a `pass` statement,
unless explicitly requested by the user. If an exception is caught and ignored for control
flow reasons, it must still be logged so that debugging is possible.

See `.agents/skills/gfplus_logging/SKILL.md` for the full logging API.
