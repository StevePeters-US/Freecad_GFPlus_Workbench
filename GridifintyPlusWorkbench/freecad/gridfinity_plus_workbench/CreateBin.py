import FreeCAD, FreeCADGui, Part
from PySide import QtGui
import os
from freecad.gridfinity_plus_workbench.CreateBinTaskPanel import BinTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources", "icons")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "resources")

class CreateBin:
    def __init__(self):
        self.taskPanel = None

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "layout-bottom-2-line.svg"),
            "Accel": "Shift+S",
            "MenuText": "Create Bin",
            "ToolTip": "Creates a bin"
        }

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        return True

    def showTaskPanel(self):
        self.taskPanel = BinTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def CreateBin(self, NumX, NumY, selection, Height):
        self.CreateTabs(NumX, NumY, selection)
        self.create_bin_shape(NumX, NumY, Height)
        self.perform_fusion(NumX, NumY)

    def CreateTabs(self, NumX, NumY, selection):
        doc = FreeCAD.ActiveDocument or FreeCAD.newDocument("Unnamed")
        
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedTab_"):
                doc.removeObject(obj.Name)
        
        tab_shape = self.load_template_shape(os.path.join(TEMPLATE_DIR, "GF+TabTemplate.FCStd"))
        blank_shape = self.load_template_shape(os.path.join(TEMPLATE_DIR, "GF+BlankTemplate.FCStd"))
        connector_shape = self.load_template_shape(os.path.join(TEMPLATE_DIR, "GF+TabConnectorTemplate.FCStd"), "Pad005")
        
        for x in range(NumX):
            for y in range(NumY):
                for slice in range(4):
                    new_body = doc.addObject('Part::Feature', f'ImportedTab_{x}_{y}_{slice}')
                    new_body.Shape = tab_shape if self.should_add_tab(x, y, slice, selection, NumX, NumY) else blank_shape
                    self.set_tab_placement(new_body, x, y, slice)
                    new_body.ViewObject.ShapeColor = (0.8, 0.0, 0.75)
        
        new_connector_body = doc.addObject('Part::Feature', 'ImportedTab_Connector')
        new_connector_body.Shape = connector_shape
        new_connector_body.ViewObject.ShapeColor = (0.8, 0.0, 0.75)
        
        doc.recompute()

    def load_template_shape(self, filepath, feature_name=None):
        doc = FreeCAD.open(filepath)
        feature = doc.getObject(feature_name) if feature_name else self.find_last_feature(doc)
        shape = feature.Shape.copy()
        FreeCAD.closeDocument(doc.Name)
        return shape

    @staticmethod
    def find_last_feature(doc):
        return next((obj for obj in reversed(doc.Objects) if obj.TypeId.startswith('PartDesign::')), None)

    @staticmethod
    def should_add_tab(x, y, slice, selection, NumX, NumY):
        if selection == 'fill':
            return True
        if selection == 'edges':
            return (x == 0 and slice == 0) or (x == NumX - 1 and slice == 2) or \
                   (y == 0 and slice == 1) or (y == NumY - 1 and slice == 3)
        if selection == 'corners':
            return ((x == 0 and y == 0 and slice in (0, 1)) or
                    (x == NumX - 1 and y == NumY - 1 and slice in (2, 3)) or
                    (y == 0 and x == NumX - 1 and slice in (1, 2)) or
                    (y == NumY - 1 and x == 0 and slice in (3, 0)))
        return False

    @staticmethod
    def set_tab_placement(body, x, y, slice):
        rot = body.Placement.Rotation.multiply(FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), slice * 90))
        center = FreeCAD.Vector(-20.75, 0, 0)
        pos = body.Placement.Base + FreeCAD.Vector(x * 42, y * 42, 0) - center
        body.Placement = FreeCAD.Placement(pos + center, rot, center)

    def create_bin_shape(self, NumX, NumY, Height):
        doc = FreeCAD.ActiveDocument or FreeCAD.newDocument("Unnamed")
        
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedBin"):
                doc.removeObject(obj.Name)
        
        bin_shape = self.load_bin_template(NumX, NumY, Height)
        new_bin_body = doc.addObject('Part::Feature', 'ImportedBin')
        new_bin_body.Shape = bin_shape
        new_bin_body.ViewObject.ShapeColor = (0.718, 0.0, 1.0)
        
        doc.recompute()

    def load_bin_template(self, NumX, NumY, Height):
        bin_doc = FreeCAD.open(os.path.join(TEMPLATE_DIR, "GF+BinTemplate.FCStd"))
        spreadsheet = bin_doc.getObject("Spreadsheet")
        if spreadsheet:
            spreadsheet.set("SizeX", str(NumX))
            spreadsheet.set("SizeY", str(NumY))
            spreadsheet.set("SizeZ", str(Height))
            bin_doc.recompute()
        bin_feature = bin_doc.getObject('Pad')
        shape = bin_feature.Shape.copy()
        FreeCAD.closeDocument(bin_doc.Name)
        return shape

    def perform_fusion(self, NumX, NumY):
        doc = FreeCAD.ActiveDocument
        workbench_objects = [obj for obj in doc.Objects if obj.Label.startswith(('ImportedTab', 'ImportedBin'))]
        connector = next((obj for obj in workbench_objects if obj.Label == 'ImportedTab_Connector'), None)
        
        if not connector or len(workbench_objects) < 2:
            QtGui.QMessageBox.information(None, "Boolean Fusion", "Fusion cannot be performed.")
            return

        shapes_for_fusion = [obj.Shape for obj in [connector] + workbench_objects if obj != connector]
        compound = Part.makeCompound(shapes_for_fusion)
        fusion = doc.addObject("Part::Feature", f"GFPlus_Bin_{NumX}_{NumY}")
        fusion.Shape = compound
        fusion.ViewObject.ShapeColor = (0.0, 0.88, 0.11)

        for obj in workbench_objects:
            doc.removeObject(obj.Name)

        doc.recompute()

FreeCADGui.addCommand('CreateBinCommand', CreateBin())
