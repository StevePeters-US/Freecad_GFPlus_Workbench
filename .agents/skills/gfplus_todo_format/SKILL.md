---
name: GFPlus Todo List Format
description: Reference for writing todo_*.md task lists. Required reading before creating a new todo file or adding tasks to an existing one.
---

# GFPlus Todo List Format

Task lists are structured markdown documents consumed by both human developers and AI agents.
Every task must be atomic, self-contained, and include enough context that the agent never
needs to guess what file to edit or what the code should look like.

---

## File Naming

```
todo_{topic}.md
```

One file per coherent feature area. Do not mix unrelated areas in one file.

---

## Document Structure

```markdown
# Gridfinity+ Workbench — {Topic} Task List

> Tasks are ordered by priority. Each task is atomic and self-contained.
> Each task includes the exact file(s) and line numbers to change.

---

## Background

{2–4 paragraph explanation of why this work is needed, what the current state is,
and what the goal state looks like after all tasks are done.}

### Key APIs

| Symbol | Location | Purpose |
|--------|----------|---------|
| `SymbolName` | `path/to/file.py:line` | One-line description |

---

## Tier 1 — {Name} (Do First)

{One-sentence description of what this tier accomplishes.}

### {PREFIX}-001: {Task title}
...

---

## Agent Skills

See `.agents/skills/` for project-specific knowledge:

| Skill | Purpose |
|-------|---------|
| `gfplus_logging` | Logging API and conventions |
| `gfplus_template_loading` | FCStd template open/extract/close pattern |
| `gfplus_command_pattern` | Command + task panel structure |

See `.agents/workflows/` for executable workflows:

| Workflow | Purpose |
|----------|---------|
| `/fix-task` | Fix a single task by ID |
```

---

## Task Format

```markdown
### {PREFIX}-{NNN}: {Short imperative title}

**File:** `path/to/file.py` — description of where (line N or "after ClassName.method()")

**What:** One or two sentences describing what this task adds or changes.

**Implementation:**
{Python code block showing exactly what to write, or a numbered algorithm.}

**Depends on:** {PREFIX}-NNN   ← omit if no dependencies
```

Completed tasks are marked `### [x] PREFIX-NNN: title`. Pending tasks have no prefix.

---

## Task Writing Rules

1. **Exact file + location** — always specify file path and line number or insertion point.
2. **Show the code** — include the full code block; never just describe it in prose.
3. **One change per task** — one method, one file section. Split if it spans two files.
4. **List direct dependencies only** — not transitive.

---

## Task ID Prefix Convention

| File | Prefix | Example |
|------|--------|---------|
| `todo_bin.md` | `B` | `B-001` |
| `todo_baseplate.md` | `P` | `P-001` |
| `todo_refactor.md` | `X` | `X-001` |

Never reuse IDs of deleted tasks.
