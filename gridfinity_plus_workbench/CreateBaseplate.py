import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import os
from freecad.gridfinity_plus_workbench.CreateBaseplateTaskPanel import BaseplateTaskPanel


ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")

class CreateBaseplate:
    def __init__(self):
        self.taskPanel = None
        self.baseplate_doc_path = None

    def GetResources(self):
        return {
            "Pixmap": str(ICONPATH + "layout-grid-line.svg"),
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
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument("Unnamed")
        
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedBaseplate"):
                doc.removeObject(obj.Name)
        
        # Get the directory of the current script
        script_path = os.path.abspath(__file__)
        template_dir = os.path.dirname(script_path) + "/resources"
        
        baseplate_doc_file_path = os.path.join(template_dir, "Gridfinity+Base_Template.FCStd")
        baseplate_doc = FreeCAD.open(baseplate_doc_file_path)

        if not baseplate_doc:
            print("Failed to set up the baseplate document.")
            return
        
        spreadsheet = baseplate_doc.getObject("Spreadsheet")
        if spreadsheet:
            try:
                spreadsheet.set("SizeX", str(NumX))
                spreadsheet.set("SizeY", str(NumY))
                baseplate_doc.recompute()
            except Exception as e:
                print(f"Error setting spreadsheet parameters: {e}")
        
        feature_name = 'Cut'
        baseplate_feature = baseplate_doc.getObject(feature_name)
        
        if not baseplate_feature:
            print(f"No feature named '{feature_name}' found in the baseplate document.")
            return

        new_baseplate_body = doc.addObject('Part::Feature', 'ImportedBaseplate')
        new_baseplate_body.Shape = baseplate_feature.Shape
        view_object = new_baseplate_body.ViewObject
        view_object.ShapeColor = (0.25, 0.25, 0.25)

        doc.recompute()
        
        try:
            FreeCAD.closeDocument(baseplate_doc.Name)
        except Exception as e:
            print(f"Error closing the baseplate document: {e}")

FreeCADGui.addCommand("CreateBaseplateCommand", CreateBaseplate())




