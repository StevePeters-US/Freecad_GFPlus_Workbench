---
name: GFPlus Command Pattern
description: How FreeCAD commands and Qt task panels are structured in this workbench. Required reading before adding or modifying any command or task panel.
---

# GFPlus Command Pattern

Every tool in this workbench consists of two classes:

1. **Command class** — registered with `FreeCADGui.addCommand()`; owns the business logic.
2. **TaskPanel class** — Qt widget shown in the FreeCAD Task panel; collects inputs and
   calls the command.

---

## Command Class Structure

```python
class CreateFoo:
    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "icon.svg"),
            "Accel": "Shift+F",
            "MenuText": "Create Foo",
            "ToolTip": "Creates a foo",
        }

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None  # or True if no document required

    def showTaskPanel(self):
        self.taskPanel = FooTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def CreateFoo(self, param1, param2):
        # Business logic here — no Qt code
        doc = FreeCAD.ActiveDocument or FreeCAD.newDocument("Unnamed")
        ...

FreeCADGui.addCommand("CreateFooCommand", CreateFoo())
```

---

## TaskPanel Class Structure

```python
from PySide import QtGui

class FooTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()

        # ... add widgets to layout ...

        self.createButton = QtGui.QPushButton("Create Foo")
        self.createButton.clicked.connect(self._onCreate)
        layout.addWidget(self.createButton)
        self.form.setLayout(layout)

    def _onCreate(self):
        # Read inputs, validate, then call command
        param1 = self.input1.value()
        self.command.CreateFoo(param1, ...)
```

---

## Registration

At the bottom of the command module:

```python
FreeCADGui.addCommand("CreateFooCommand", CreateFoo())
```

The command string `"CreateFooCommand"` must also be added to `init_gui.py`:

```python
self.list = ["CreateBaseplateCommand", "CreateBinCommand", "CreateFooCommand"]
```

---

## Rules

- The command class owns **all** business logic — the task panel only collects and validates input.
- `IsActive()` must return `FreeCAD.ActiveDocument is not None` for commands that modify the document.
- Task panels do not import `Part` or manipulate FreeCAD objects directly.
- Do not call `FreeCADGui.Control.closeDialog()` from inside the task panel — let the user close it.

---

## Files to Read Before Editing

1. `freecad/gridfinity_plus_workbench/CreateBin.py` — reference command implementation
2. `freecad/gridfinity_plus_workbench/CreateBinTaskPanel.py` — reference task panel
3. `freecad/gridfinity_plus_workbench/init_gui.py` — where commands are registered in the workbench
