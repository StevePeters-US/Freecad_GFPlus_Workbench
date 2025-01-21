import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore
import math

class BaseplateTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()

        # NumX input
        self.labelNumX = QtGui.QLabel("NumX:")
        self.layout.addWidget(self.labelNumX)
        self.numXInput = QtGui.QSpinBox()
        self.numXInput.setMinimum(1)
        self.numXInput.setValue(1)
        self.layout.addWidget(self.numXInput)

        # NumY input
        self.labelNumY = QtGui.QLabel("NumY:")
        self.layout.addWidget(self.labelNumY)
        self.numYInput = QtGui.QSpinBox()
        self.numYInput.setMinimum(1)
        self.numYInput.setValue(1)
        self.layout.addWidget(self.numYInput)

        # Create button
        self.createButton = QtGui.QPushButton("Create Baseplate")
        self.createButton.clicked.connect(self.CreateBaseplate)
        self.layout.addWidget(self.createButton)

        self.form.setLayout(self.layout)

    def CreateBaseplate(self):
        numX = self.numXInput.value()
        numY = self.numYInput.value()
        self.command.CreateBaseplate(numX, numY)

class CommandCreateBaseplate:
    def GetResources(self):
        return {'Pixmap': 'path/to/icon.svg',
                'MenuText': 'Create Baseplate',
                'ToolTip': 'Create a new baseplate'}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        FreeCADGui.Control.showDialog(BaseplateTaskPanel(self))

def CreateBaseplate(numX, numY):
    print(f"Creating Baseplate with NumX: {numX}, NumY: {numY}")

FreeCADGui.addCommand('CreateBaseplate', CommandCreateBaseplate())

# To open the task panel, execute the command:
FreeCADGui.runCommand('CreateBaseplate')