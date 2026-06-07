---
name: GFPlus Code Review Process
description: How to conduct a scoped code review of this workbench. Defines the file map, universal checklist, findings format, and triage workflow.
---

# GFPlus Code Review Process

Review one subsystem at a time. The codebase is small, but keeping reviews focused prevents
shallow findings.

---

## Step 0 — Pre-Review Context

Load these before reading any source file:

1. `AGENTS.md` — conventions and architectural rules
2. `INDEX.md` — file map, known bugs, development patterns
3. Relevant skills from the Skill Dispatch Table

---

## Step 1 — Pick One Subsystem

| Subsystem | Files to Review |
|-----------|-----------------|
| **Bin Command** | `CreateBin.py`, `CreateBinTaskPanel.py` |
| **Baseplate Command** | `CreateBaseplate.py`, `CreateBaseplateTaskPanel.py` |
| **Workbench Init** | `init_gui.py` |

---

## Step 2 — File Traversal Rules

For each file:
1. Read the full file.
2. Note class names, method names, and any `TODO`/`FIXME` comments.
3. Apply the universal checklist (Step 3).
4. Note findings immediately — do not defer.

---

## Step 3 — Universal Checklist

| # | Check | Violation pattern |
|---|-------|-------------------|
| U1 | No `print()` calls | `print(` anywhere in production code |
| U2 | Every `except` block logs via `FreeCAD.Console` | `except ...: pass` or bare `except` with no log |
| U3 | `IsActive()` checks `FreeCAD.ActiveDocument is not None` for doc-mutating commands | `return True` when the command writes to the document |
| U4 | Template docs are always closed after shape extraction | `FreeCAD.open()` without matching `FreeCAD.closeDocument()` |
| U5 | Shape is `.copy()`-ed before the template doc is closed | `shape = feature.Shape` (no copy) |
| U6 | `doc.recompute()` called after writing spreadsheet values | spreadsheet writes without subsequent `recompute()` |
| U7 | FreeCADGui command registered at module level | missing `FreeCADGui.addCommand(...)` at end of file |
| U8 | Import order: FreeCAD → PySide → project → stdlib | check imports block |
| U9 | All log messages end with `\n` | `PrintMessage("text")` without trailing newline |

---

## Step 4 — Findings Format

Write findings to `code_review.md` at the repo root:

```markdown
### [SUBSYSTEM] SEVERITY: Short title

**File:** `path/to/file.py:line`
**Issue:** One sentence describing the violation.
**Convention:** Which rule or skill this violates (e.g. "U1 — print() call", "U4 — template not closed").
**Fix:** (optional) What to change.
```

Severity levels:
- **BUG** — will crash or produce wrong results at runtime
- **CONVENTION** — violates a documented project convention
- **SMELL** — works but inconsistent with established patterns

---

## Step 5 — Triage

| Bucket | Criteria | Action |
|--------|----------|--------|
| **Fix now** | Small, self-contained, no design questions | Fix inline; prefix with `[FIXED]` in `code_review.md` |
| **Add to todo** | Valid but non-trivial | Add to `todo_*.md` using `gfplus_todo_format/SKILL.md`; prefix with `[TODO: PREFIX-NNN]` |
| **Document** | Intentional design choice | Clarify in `AGENTS.md`; prefix with `[DOCUMENTED]` |
| **Discard** | Misunderstands architecture | Prefix with `[DISCARDED: reason]` |

---

## Architectural Guardrails

Do NOT flag these without explicit user approval:

| Agent flags... | Reality |
|----------------|---------|
| "Remove template close/open round-trip" | Intentional — shapes must be extracted from the template's document context |
| "Merge CreateBin and BinTaskPanel into one file" | Out of scope unless user requests it |
| "Add type hints" | Out of scope unless user requests it |
| "Split this method" | Scope control — do not refactor without explicit request |
| "Use `Part.makeShell` instead of compound" | Design decision — do not change without user approval |

---

## Files to Read Before Starting

1. `AGENTS.md`
2. `INDEX.md`
3. Skills for the chosen subsystem (see Skill Dispatch Table in `INDEX.md`)
