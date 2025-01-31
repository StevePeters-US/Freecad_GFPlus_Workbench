import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore

class BinTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()

        # NumX range input
        self.labelNumXRange = QtGui.QLabel("NumX Range:")
        self.layout.addWidget(self.labelNumXRange)
        self.numXMinInput = QtGui.QSpinBox()
        self.numXMinInput.setMinimum(1)
        self.numXMinInput.setValue(1)
        self.layout.addWidget(self.numXMinInput)
        self.numXMaxInput = QtGui.QSpinBox()
        self.numXMaxInput.setMinimum(1)
        self.numXMaxInput.setValue(1)
        self.layout.addWidget(self.numXMaxInput)

        # NumY range input
        self.labelNumYRange = QtGui.QLabel("NumY Range:")
        self.layout.addWidget(self.labelNumYRange)
        self.numYMinInput = QtGui.QSpinBox()
        self.numYMinInput.setMinimum(1)
        self.numYMinInput.setValue(1)
        self.layout.addWidget(self.numYMinInput)
        self.numYMaxInput = QtGui.QSpinBox()
        self.numYMaxInput.setMinimum(1)
        self.numYMaxInput.setValue(1)
        self.layout.addWidget(self.numYMaxInput)

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
        numXMin = self.numXMinInput.value()
        numXMax = self.numXMaxInput.value()
        numYMin = self.numYMinInput.value()
        numYMax = self.numYMaxInput.value()
        selection = self.enumInput.currentText()
        height = self.heightInput.value()
        
        for numX in range(numXMin, numXMax + 1):
            for numY in range(numYMin, numYMax + 1):
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


