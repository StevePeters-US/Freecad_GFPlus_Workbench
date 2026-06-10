import FreeCAD, FreeCADGui
import os
from freecad.gridfinity_plus_workbench.LayoutBinsTaskPanel import LayoutBinsTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources", "icons")

GRID_SPACING = 42
LAYOUT_COLOR = (0.0, 0.75, 0.9)    # cyan
PREVIEW_COLOR = (1.0, 0.85, 0.0)   # yellow
PREVIEW_TRANSPARENCY = 70


class LayoutBins:
    def __init__(self):
        self.taskPanel = None

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "layout-top-2-line.svg"),
            "MenuText": "Layout Bins",
            "ToolTip": "Arrange bins on the baseplate at grid positions",
        }

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        return True

    def showTaskPanel(self):
        self.taskPanel = LayoutBinsTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def PlaceLayout(self, entries):
        doc = FreeCAD.ActiveDocument
        if not doc:
            FreeCAD.Console.PrintWarning("[GFPlus] LayoutBins.PlaceLayout: no active document.\n")
            return
        self._clear_objects(doc, "LayoutBin_")
        self._clear_objects(doc, "PreviewBin_")
        self._place(doc, entries, prefix="LayoutBin", color=LAYOUT_COLOR, transparency=0)
        doc.recompute()

    def PlacePreview(self, entries):
        doc = FreeCAD.ActiveDocument
        if not doc:
            return
        self._clear_objects(doc, "PreviewBin_")
        self._place(doc, entries, prefix="PreviewBin", color=PREVIEW_COLOR, transparency=PREVIEW_TRANSPARENCY)
        doc.recompute()

    def ClearPreview(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            self._clear_objects(doc, "PreviewBin_")
            doc.recompute()

    @staticmethod
    def _clear_objects(doc, prefix):
        for obj in list(doc.Objects):
            if obj.Name.startswith(prefix):
                doc.removeObject(obj.Name)

    @staticmethod
    def _place(doc, entries, prefix, color, transparency):
        for entry in entries:
            src = doc.getObject(entry['bin_name'])
            if src is None:
                FreeCAD.Console.PrintWarning(
                    f"LayoutBins: bin '{entry['bin_name']}' not found, skipping.\n"
                )
                continue

            gx = entry['grid_x']
            gy = entry['grid_y']
            placed = doc.addObject('Part::Feature', f"{prefix}_{gx}_{gy}")
            placed.Shape = src.Shape.copy()
            placed.Placement = FreeCAD.Placement(
                FreeCAD.Vector(gx * GRID_SPACING, gy * GRID_SPACING, 0),
                FreeCAD.Rotation(),
            )
            placed.ViewObject.ShapeColor = color
            placed.ViewObject.Transparency = transparency


FreeCADGui.addCommand('LayoutBinsCommand', LayoutBins())
