import FreeCAD, FreeCADGui, Part, Sketcher
from PySide import QtGui, QtCore

class TabsTaskPanel:
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

        # Create button
        self.createButton = QtGui.QPushButton("Create Tab")
        self.createButton.clicked.connect(self.CreateTabs)
        self.layout.addWidget(self.createButton)

        self.form.setLayout(self.layout)

    def CreateTabs(self):
        numX = self.numXInput.value()
        numY = self.numYInput.value()
        selection = self.enumInput.currentText()
        self.command.CreateTabs(numX, numY, selection)

class CommandCreateTabs:
    def GetResources(self):
        return {'Pixmap': 'path/to/icon.svg',
                'MenuText': 'Create Tab',
                'ToolTip': 'Create a new Tab'}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        FreeCADGui.Control.showDialog(TabsTaskPanel(self))

def CreateTabs(numX, numY, selection):
    print(f"Creating Tab with NumX: {numX}, NumY: {numY}, Selection: {selection}")

FreeCADGui.addCommand('CreateTabs', CommandCreateTabs())

# To open the task panel, execute the command:
FreeCADGui.runCommand('CreateTabs')
