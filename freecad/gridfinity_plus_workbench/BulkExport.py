import os
import FreeCAD, FreeCADGui, Part
from freecad.gridfinity_plus_workbench.BulkExportTaskPanel import BulkExportTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources", "icons")


class BulkExport:
    def __init__(self):
        self.taskPanel = None

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "checkbox-multiple-blank-line.svg"),
            "MenuText": "Bulk Export",
            "ToolTip": "Export multiple GFPlus objects as individual STL or STEP files",
        }

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def showTaskPanel(self):
        self.taskPanel = BulkExportTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def ExportObjects(self, objects, folder, fmt):
        exported = []
        failed = []
        for obj in objects:
            ok = True
            if fmt in ("STL", "Both"):
                try:
                    obj.Shape.exportStl(os.path.join(folder, obj.Name + ".stl"))
                except Exception as e:
                    FreeCAD.Console.PrintError(f"[GFPlus] BulkExport: STL export failed for {obj.Name}: {e}\n")
                    ok = False
            if fmt in ("STEP", "Both"):
                try:
                    Part.export([obj], os.path.join(folder, obj.Name + ".step"))
                except Exception as e:
                    FreeCAD.Console.PrintError(f"[GFPlus] BulkExport: STEP export failed for {obj.Name}: {e}\n")
                    ok = False
            if ok:
                exported.append(obj.Name)
                FreeCAD.Console.PrintMessage(f"[GFPlus] BulkExport: exported {obj.Name}\n")
            else:
                failed.append(obj.Name)
        return exported, failed


FreeCADGui.addCommand('BulkExportCommand', BulkExport())
