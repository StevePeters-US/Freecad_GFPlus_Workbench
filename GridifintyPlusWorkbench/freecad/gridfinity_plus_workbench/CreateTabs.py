import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import os
import math
from freecad.gridfinity_plus_workbench.CreateTabsTaskPanel import TabsTaskPanel

ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")

class CreateTabs:
    def __init__(self):
        self.taskPanel = None
    
    def GetResources(self):
        return {"Pixmap"  : str(ICONPATH + "layout-grid-fill.svg"),  
                "Accel"   : "Shift+S",  # a default shortcut (optional)
                "MenuText": "Create Tabs",
                "ToolTip" : "Customize the tabs that connect the bins to the baseplate"}
    
    def Activated(self):
        self.showTaskPanel()
    
    def IsActive(self):
        """Define when the command is active (optional)"""
        return True
    
    def showTaskPanel(self):
        self.taskPanel = TabsTaskPanel(self)
        FreeCADGui.Control.showDialog(self.taskPanel)
    
    def CreateTabs(self, NumX, NumY, selection):
        # Get the active document
        doc = FreeCAD.ActiveDocument
        
        # Create a new document if none exists
        if doc is None:
            doc = FreeCAD.newDocument("Unnamed")
                
        # Delete all previously created bodies
        for obj in doc.Objects:
            if obj.Name.startswith("ImportedTab_"):
                doc.removeObject(obj.Name)
        
        # Get the directory of the current script
        script_path = os.path.abspath(__file__)
        template_dir = os.path.dirname(script_path) + "/resources"
        
        tab_doc_file_path = os.path.join(template_dir, "GF+TabTemplate.FCStd")
        blank_doc_file_path = os.path.join(template_dir, "GF+BlankTemplate.FCStd")
        connector_doc_file_path = os.path.join(template_dir, "GF+TabConnectorTemplate.FCStd")

        # Ensure we close the documents before loading them again
        documents_to_close = ["GF+TabTemplate", "GF+BlankTemplate", "GF+TabConnectorTemplate"]
        for doc_name in documents_to_close:
            if doc_name in FreeCAD.listDocuments():
                FreeCAD.closeDocument(doc_name)

        # Load the stored body files
        tab_doc = FreeCAD.open(tab_doc_file_path)
        blank_doc = FreeCAD.open(blank_doc_file_path)
        connector_doc = FreeCAD.open(connector_doc_file_path)
        
        
        # Find the last feature in the body (last operation)
        tab_feature = None
        for obj in tab_doc.Objects:
            if obj.TypeId.startswith('PartDesign::'):
                tab_feature = obj
        
        if tab_feature is None:
            print("No valid PartDesign feature found in the loaded document.")
            return
        
        blank_feature = None
        for obj in blank_doc.Objects:
            if obj.TypeId.startswith('PartDesign::'):
                blank_feature = obj

        if blank_feature is None:
            print("No valid PartDesign feature found in the blank document.")
            return
        
        # Perform the array operation
        for x in range(NumX):
            for y in range(NumY):
                for slice in range(4):
                        # Use tab_feature for the outer edge wedges
                    new_body = doc.addObject('Part::Feature', f'ImportedTab_{x}_{y}_{slice}')
                    addTab = False
                    
                    if selection == 'fill':
                        addTab = True

                    elif (selection == 'edges'):
                        if  ((x == 0 and slice == 0) or
                            (x == NumX - 1 and slice == 2) or
                            (y == 0 and slice == 1) or
                            (y == NumY - 1 and slice ==3)):
                            addTab = True

                    elif (selection == 'corners'):
                        if ((x == 0 and y == 0 and (slice == 0 or slice == 1)) or
                        (x == NumX - 1 and  y == NumY - 1 and (slice == 2 or slice == 3)) or
                        (y == 0 and x == NumX - 1 and (slice == 1 or slice == 2)) or
                        (y == NumY - 1 and x == 0 and (slice ==3 or slice == 0))):
                            addTab = True
                        else:
                            addTab = False

                    elif (selection == 'none'):
                        addTab = False

                    if addTab == True:
                        new_body.Shape = tab_feature.Shape
                    else:
                        # Use blank_feature for other positions
                        new_body.Shape = blank_feature.Shape 

                    rot = new_body.Placement.Rotation.multiply(FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), slice * 90))
                    center = FreeCAD.Vector(-20.75, 0, 0)  

                    # Calculate the new position, considering the rotation center
                    pos = new_body.Placement.Base + FreeCAD.Vector(x * 42, y * 42, 0) - center

                    # Apply the new placement with the rotation and the correct center
                    new_body.Placement = FreeCAD.Placement(pos + center, rot, center)

                    view_object = new_body.ViewObject
                    view_object.ShapeColor = (0.8, 0.0, 0.75)  

        # Access and modify the spreadsheet in the bin document
        spreadsheet = connector_doc.getObject("Spreadsheet")
        if spreadsheet:
            # Adjust parameters as needed
            spreadsheet.set("SizeX", str(NumX))
            spreadsheet.set("SizeY", str(NumY))
            connector_doc.recompute()

        feature_name = 'Pad005'
        connector_feature = connector_doc.getObject(feature_name)

        if connector_feature is None:
            print(f"No feature named {feature_name} found in the bin document.")
            return
        
        new_connector_body = doc.addObject('Part::Feature', 'ImportedTab_Connector')
        new_connector_body.Shape = connector_feature.Shape
        view_object = new_connector_body.ViewObject
        view_object.ShapeColor = (0.8, 0.0, 0.75) 

        doc.recompute()
        
        # Close the stored documents after copying
        FreeCAD.closeDocument(tab_doc.Name)
        FreeCAD.closeDocument(blank_doc.Name)
        FreeCAD.closeDocument(connector_doc.Name)

FreeCADGui.addCommand('CreateTabsCommand', CreateTabs())

