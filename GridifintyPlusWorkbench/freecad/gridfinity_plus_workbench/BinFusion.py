import FreeCAD, FreeCADGui, Part
from PySide import QtGui, QtCore
import os

ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")

class BinFusionTool:
    def GetResources(self):
        return {'Pixmap': str(ICONPATH + "checkbox-multiple-blank-line.svg"),  
                'MenuText': 'Fusion',
                'ToolTip': 'Fuse all objects created by the workbench'}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        self.perform_fusion()

    def perform_fusion(self):
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
        fusion = doc.addObject("Part::Feature", "BinFusion")
        fusion.Shape = compound

        view_object = fusion.ViewObject
        view_object.ShapeColor = (0.0, 0.88, 0.11)  

        # Recompute the document to update the changes
        doc.recompute()

        # Delete the used imported bodies
        for obj in workbench_objects:
            doc.removeObject(obj.Name)
        doc.removeObject(importedbody_connector.Name)

FreeCADGui.addCommand('BinFusionTool', BinFusionTool())

# To run the tool, execute the command:
FreeCADGui.runCommand('BinFusionTool')
