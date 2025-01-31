import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import os
from freecad.gridfinity_plus_workbench.CreateBaseplateTaskPanel import BaseplateTaskPanel

class CreateBaseplate:
    def __init__(self):
        self.taskPanel = None
        self.ICONPATH = os.path.join(os.path.dirname(__file__), "resources", "icons")
        self.TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "resources")
        self.TEMPLATE_FILE = "Gridfinity+Base_Template.FCStd"
        self.FEATURE_NAME = 'Cut001'

    def GetResources(self):
        return {
            "Pixmap": os.path.join(self.ICONPATH, "layout-grid-line.svg"),
            "Accel": "Shift+S",
            "MenuText": "Create GF+ Baseplate",
            "ToolTip": "Create GF+ Baseplate"
        }

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        return True

    def showTaskPanel(self):
        self.taskPanel = BaseplateTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def CreateBaseplate(self, NumX, NumY):
        doc = self._getOrCreateDocument()
        self._cleanupPreviousBaseplates(doc)
        
        baseplate_doc = self._openBaseplateTemplate()
        if not baseplate_doc:
            return

        self._updateSpreadsheet(baseplate_doc, NumX, NumY)
        baseplate_feature = self._getBaseplateFeature(baseplate_doc)
        if not baseplate_feature:
            return

        self._createNewBaseplateBody(doc, baseplate_feature, NumX, NumY)
        FreeCAD.closeDocument(baseplate_doc.Name)

    def _getOrCreateDocument(self):
        doc = FreeCAD.ActiveDocument
        return doc if doc else FreeCAD.newDocument("Unnamed")

    def _cleanupPreviousBaseplates(self, doc):
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedBaseplate"):
                doc.removeObject(obj.Name)

    def _openBaseplateTemplate(self):
        template_path = os.path.join(self.TEMPLATE_DIR, self.TEMPLATE_FILE)
        try:
            return FreeCAD.open(template_path)
        except Exception as e:
            print(f"Error opening template: {e}")
            return None

    def _updateSpreadsheet(self, doc, NumX, NumY):
        spreadsheet = doc.getObject("Spreadsheet")
        if spreadsheet:
            spreadsheet.set("SizeX", str(NumX))
            spreadsheet.set("SizeY", str(NumY))
            doc.recompute()
        else:
            print("Spreadsheet not found in the template.")

    def _getBaseplateFeature(self, doc):
        feature = doc.getObject(self.FEATURE_NAME)
        if not feature:
            print(f"No feature named {self.FEATURE_NAME} found in the baseplate document.")
        return feature

    def _createNewBaseplateBody(self, doc, baseplate_feature, NumX, NumY):
        new_baseplate_body = doc.addObject('Part::Feature', f'GFPlus_Baseplate_{NumX}_{NumY}')
        new_baseplate_body.Shape = baseplate_feature.Shape
        view_object = new_baseplate_body.ViewObject
        view_object.ShapeColor = (0.25, 0.25, 0.25)
        doc.recompute()

FreeCADGui.addCommand("CreateBaseplateCommand", CreateBaseplate())
