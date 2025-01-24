import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore

class BinTaskPanel:
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

        # Enum input
        self.labelEnum = QtGui.QLabel("Selection:")
        self.layout.addWidget(self.labelEnum)
        self.enumInput = QtGui.QComboBox()
        self.enumInput.addItems(["edges", "corners", "fill", "none"])
        self.layout.addWidget(self.enumInput)

        # Height input
        self.labelHeight = QtGui.QLabel("Height:")
        self.layout.addWidget(self.labelHeight)
        self.heightInput = QtGui.QDoubleSpinBox()
        self.heightInput.setMinimum(0.0)
        self.heightInput.setMaximum(359.0)
        self.heightInput.setValue(0.75)
        self.layout.addWidget(self.heightInput)

        # Create button
        self.createButton = QtGui.QPushButton("Create Bin")
        self.createButton.clicked.connect(self.CreateBin)
        self.layout.addWidget(self.createButton)

        self.form.setLayout(self.layout)

    def CreateBin(self):
        numX = self.numXInput.value()
        numY = self.numYInput.value()
        selection = self.enumInput.currentText()
        height = self.heightInput.value()
        self.command.CreateBin(numX, numY, selection, height)

class CommandCreateBin:
    def GetResources(self):
        return {'Pixmap': 'path/to/icon.svg',
                'MenuText': 'Create Bin',
                'ToolTip': 'Create a new bin'}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        FreeCADGui.Control.showDialog(BinTaskPanel(self))

def CreateBin(numX, numY, selection, height):
    print(f"Creating bin with NumX: {numX}, NumY: {numY}, Selection: {selection}, Height: {height}")

FreeCADGui.addCommand('CreateBin', CommandCreateBin())

# # To open the task panel, execute the command:
# FreeCADGui.runCommand('CreateBin')
