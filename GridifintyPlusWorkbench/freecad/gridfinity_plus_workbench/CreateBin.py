import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import os
import math
from freecad.gridfinity_plus_workbench.CreateBinTaskPanel import BinTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")

class CreateBin:
    def __init__(self):
        self.taskPanel = None
    
    def GetResources(self):
        return {"Pixmap"  : str(ICONPATH + "layout-bottom-2-line.svg"),  
                "Accel"   : "Shift+S",  # a default shortcut (optional)
                "MenuText": "Create Bin",
                "ToolTip" : "Creates a bin"}
    
    def Activated(self):
        self.showTaskPanel()
    
    def IsActive(self):
        """Define when the command is active (optional)"""
        return True
    
    def showTaskPanel(self):
        self.taskPanel = BinTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)
    
    def CreateBin(self, NumX, NumY, Height):
        # Get the active document
        doc = FreeCAD.ActiveDocument
        
        # Create a new document if none exists
        if doc is None:
            doc = FreeCAD.newDocument("Unnamed")
        
        # Delete all previously created bodies
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedBin"):
                doc.removeObject(obj.Name)
        
        # Get the directory of the current script
        script_path = os.path.abspath(__file__)
        template_dir = os.path.dirname(script_path) + "/resources"
        
        bin_doc_file_path = os.path.join(template_dir, "GF+BinTemplate.FCStd")

        # Ensure we close the documents before loading them again
        documents_to_close = ["GF+BinTemplate"]
        for doc_name in documents_to_close:
            if doc_name in FreeCAD.listDocuments():
                FreeCAD.closeDocument(doc_name)

        bin_doc = FreeCAD.open(bin_doc_file_path)
        
        # Access and modify the spreadsheet in the bin document
        spreadsheet = bin_doc.getObject("Spreadsheet")
        if spreadsheet:
            # Adjust parameters as needed
            spreadsheet.set("SizeX", str(NumX))
            spreadsheet.set("SizeY", str(NumY))
            spreadsheet.set("SizeZ", str(Height))
            bin_doc.recompute()

        # Replace 'YourFeatureName' with the actual name of the feature you're looking for
        feature_name = 'Pad'

        # # List all features in the bin document
        # print("List of features in the bin document:")
        # for obj in bin_doc.Objects:
        #     print(f"Name: {obj.Name}, Type: {obj.TypeId}")

        # Find the feature by name in the bin document
        bin_feature = bin_doc.getObject(feature_name)

        if bin_feature is None:
            print(f"No feature named {feature_name} found in the bin document.")
            return   
 
        # Add the new bin body
        new_bin_body = doc.addObject('Part::Feature', 'ImportedBin')
        new_bin_body.Shape = bin_feature.Shape

        view_object = new_bin_body.ViewObject
        view_object.ShapeColor = (0.718, 0.0, 1.0)  

        doc.recompute()
        
        # Close the stored documents after copying
        FreeCAD.closeDocument(bin_doc.Name)

FreeCADGui.addCommand('CreateBinCommand', CreateBin())

