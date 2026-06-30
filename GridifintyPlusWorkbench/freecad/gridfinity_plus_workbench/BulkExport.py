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
            try:
                if fmt in ("STL", "Both"):
                    path = os.path.join(folder, obj.Name + ".stl")
                    obj.Shape.exportStl(path)
                if fmt in ("STEP", "Both"):
                    path = os.path.join(folder, obj.Name + ".step")
                    Part.export([obj], path)
                exported.append(obj.Name)
                FreeCAD.Console.PrintMessage(f"BulkExport: exported {obj.Name}\n")
            except Exception as e:
                FreeCAD.Console.PrintError(f"BulkExport: failed to export {obj.Name}: {e}\n")
                failed.append(obj.Name)
        return exported, failed


FreeCADGui.addCommand('BulkExportCommand', BulkExport())
