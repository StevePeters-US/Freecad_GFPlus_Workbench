---
name: Project Index Updater
description: How and when to update INDEX.md after adding, renaming, or deleting files, classes, or skills. Required reading before any structural change to the repo.
---

# Project Index Updater

`INDEX.md` is the single source of truth for agents navigating this codebase. Keeping it
accurate eliminates expensive discovery tool calls on every new agent session.

**Rule: whenever you add, rename, or delete a file, class, or skill, you MUST update
`INDEX.md` in the same edit.**

---

## What to Update and When

### 1. File Map
**Trigger:** added, moved, or deleted a file under `freecad/gridfinity_plus_workbench/`.

Update the **File Map** table — add a row, remove the row, or update the path.

### 2. Resource Files Table
**Trigger:** added or changed a template `.FCStd` file.

Update the **Resource Files** sub-table with the file path, spreadsheet params, and output feature name.

### 3. Class → File Index
**Trigger:** added, renamed, or deleted a class anywhere in the codebase.

Update the **Class → File Index** table. Use the line number where `class Foo:` appears.

### 4. Skill Dispatch Table
**Trigger:** created a new skill in `.agents/skills/`.

Add a row: skill folder name + "If you are about to…" trigger sentence.

### 5. Known Bugs
**Trigger:** discovered a non-trivial bug that another agent is likely to hit.

Add a row with the file:line and a one-liner fix hint. Remove the row once fixed.

### 6. Development Patterns
**Trigger:** a project-wide convention changes.

Update the **Development Patterns** section.

---

## Verification

After editing `INDEX.md`:
- Confirm all file paths in the File Map exist on disk.
- Confirm all class names in the Class Index are present in the referenced file.
- Confirm all skill folder names in the Skill Dispatch Table have a `SKILL.md` file.

## Files to Read Before Editing

1. `INDEX.md` — read it fully before making changes.
