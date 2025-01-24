import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import os
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

    def perform_fusion(self, NumX, NumY):
        doc = FreeCAD.ActiveDocument
        all_objects = doc.Objects

        # Filter objects created by the workbench
        workbench_objects = [obj for obj in all_objects if obj.Label.startswith('ImportedTab') or obj.Label.startswith('ImportedBin')]

        # Find the imported body connector
        importedbody_connector = None
        for obj in workbench_objects:
            if obj.Label == 'ImportedTab_Connector':
                importedbody_connector = obj
                workbench_objects.remove(obj)
                break

        if importedbody_connector is None:
            QtGui.QMessageBox.information(None, "Boolean Fusion", "No ImportedTab_Connector found.")
            return

        if len(workbench_objects) < 1:
            QtGui.QMessageBox.information(None, "Boolean Fusion", "There should be at least one other object created by the workbench to fuse with ImportedTab_Connector.")
            return

        # Initialize the fused object with the imported body connector
        fused_object = importedbody_connector

        # Create a list to hold the shapes for fusion
        shapes_for_fusion = [fused_object.Shape]

        # Iterate through the list and collect shapes for fusion
        for obj in workbench_objects:
            shapes_for_fusion.append(obj.Shape)

        # Perform the fusion using Part.makeCompound
        compound = Part.makeCompound(shapes_for_fusion)

        # Create a new object to hold the fused shape
        fusion = doc.addObject("Part::Feature", f"GFPlus_Bin_{NumX}_{NumY}")
        fusion.Shape = compound

        view_object = fusion.ViewObject
        view_object.ShapeColor = (0.0, 0.88, 0.11)  

        # Recompute the document to update the changes
        doc.recompute()

        # Delete the used imported bodies
        for obj in workbench_objects:
            doc.removeObject(obj.Name)
        doc.removeObject(importedbody_connector.Name)

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

    def CreateBin(self, NumX, NumY, selection, Height):
        self.CreateTabs(NumX, NumY, selection)


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

        # Close the stored documents after copying
        FreeCAD.closeDocument(bin_doc.Name)

        self.perform_fusion(NumX, NumY)

        doc.recompute()
        



FreeCADGui.addCommand('CreateBinCommand', CreateBin())