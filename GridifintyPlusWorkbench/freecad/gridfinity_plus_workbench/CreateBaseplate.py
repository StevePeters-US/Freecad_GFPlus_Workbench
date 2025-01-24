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
        
        feature_name = 'Body'
        baseplate_feature = baseplate_doc.getObject(feature_name)
        
        if not baseplate_feature:
            print(f"No feature named '{feature_name}' found in the baseplate document.")
            return

  
        
        shapes_for_fusion = []

        for x in range(NumX):
            for y in range(NumY):
                new_body = doc.addObject('Part::Feature', f'ImportedBaseplate_{x}_{y}')
                print(f"New body '{new_body.Name}' created at position ({x}, {y}).")

                new_body.Shape = baseplate_feature.Shape
                
                center = FreeCAD.Vector(-20.75, 0, 0) 
                pos = new_body.Placement.Base + FreeCAD.Vector(x * 42, y * 42, 0) - center
                #rot = new_body.Placement.Rotation.multiply(FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), slice * 90))
                # Apply the new placement with the rotation and the correct center
                new_body.Placement.Base = pos
                new_body.Placement = FreeCAD.Placement(pos + center, FreeCAD.Rotation(FreeCAD.Vector(0, 0, 0), center))

                view_object = new_body.ViewObject
                view_object.ShapeColor = (0.25, 0.25, 0.25)

                shapes_for_fusion.append(new_body.Shape)
        
       

        # compound = Part.makeCompound(shapes_for_fusion)

        # fusion = doc.addObject('Part::Feature', f'Baseplate_{NumX}_{NumY}')
        # fusion.Shape = compound

        # view_object = fusion.ViewObject
        # view_object.ShapeColor = (0.0, 0.88, 0.11)


        doc.recompute()
        
        try:
            FreeCAD.closeDocument(baseplate_doc.Name)
        except Exception as e:
            print(f"Error closing the baseplate document: {e}")

FreeCADGui.addCommand("CreateBaseplateCommand", CreateBaseplate())




