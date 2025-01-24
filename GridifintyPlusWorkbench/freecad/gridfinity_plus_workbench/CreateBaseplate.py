import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import math
import os
from freecad.gridfinity_plus_workbench.CreateBaseplateTaskPanel import BaseplateTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")

class CreateBaseplate:

    def __init__(self):
        self.taskPanel = None

    def GetResources(self):
        return {"Pixmap"  : str(ICONPATH + "layout-grid-line.svg"),  
                "Accel"   : "Shift+S",  # a default shortcut (optional)
                "MenuText": "Create GF+ Baseplate",
                "ToolTip" : "Create GF+ Baseplate"}

    def Activated(self):
        self.showTaskPanel()

    def IsActive(self):
        """Define when the command is active (optional)"""
        return True

    def showTaskPanel(self):
        self.taskPanel = BaseplateTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)

    def CreateBaseplate(self, NumX, NumY):
        # Get the active document
        doc = FreeCAD.ActiveDocument
        
        # Create a new document if none exists
        if doc is None:
            doc = FreeCAD.newDocument("Unnamed")
                
        # Delete all previously created bodies
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedBaseplate"):
                doc.removeObject(obj.Name)
        
        # Get the directory of the current script
        script_path = os.path.abspath(__file__)
        template_dir = os.path.dirname(script_path) + "/resources"
        
        baseplate_doc_file_path = os.path.join(template_dir, "Gridfinity+Base_Template.FCStd")

        baseplate_doc = FreeCAD.open(baseplate_doc_file_path)
        
        # Access and modify the spreadsheet in the baseplate document
        spreadsheet = baseplate_doc.getObject("Spreadsheet")
        if spreadsheet:
            # Adjust parameters as needed
            spreadsheet.set("SizeX", str(NumX))
            spreadsheet.set("SizeY", str(NumY))
            baseplate_doc.recompute()

        # Replace 'YourFeatureName' with the actual name of the feature you're looking for
        feature_name = 'Cut001'
        baseplate_feature = baseplate_doc.getObject(feature_name)

        if baseplate_feature is None:
            print(f"No feature named {feature_name} found in the baseplate document.")
            return
        
            
            # Add the new baseplate body
        new_baseplate_body = doc.addObject('Part::Feature', 'ImportedBaseplate')
        new_baseplate_body.Shape = baseplate_feature.Shape

        # Change the color of the new baseplate body
        view_object = new_baseplate_body.ViewObject
        view_object.ShapeColor = (0.25, 0.25, 0.25)  

        doc.recompute()
        
        # Close the stored documents after copying
        FreeCAD.closeDocument(baseplate_doc.Name)




FreeCADGui.addCommand("CreateBaseplateCommand", CreateBaseplate())