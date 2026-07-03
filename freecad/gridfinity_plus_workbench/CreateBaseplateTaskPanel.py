import FreeCAD
from PySide import QtGui


class BaseplateTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()

        self.labelNumX = QtGui.QLabel("NumX:")
        self.layout.addWidget(self.labelNumX)
        self.numXInput = QtGui.QSpinBox()
        self.numXInput.setMinimum(1)
        self.numXInput.setValue(1)
        self.layout.addWidget(self.numXInput)

        self.labelNumY = QtGui.QLabel("NumY:")
        self.layout.addWidget(self.labelNumY)
        self.numYInput = QtGui.QSpinBox()
        self.numYInput.setMinimum(1)
        self.numYInput.setValue(1)
        self.layout.addWidget(self.numYInput)

        self.createButton = QtGui.QPushButton("Create Baseplate")
        self.createButton.clicked.connect(self.CreateBaseplate)
        self.layout.addWidget(self.createButton)

        self.form.setLayout(self.layout)

    def CreateBaseplate(self):
        numX = self.numXInput.value()
        numY = self.numYInput.value()
        self.command.CreateBaseplate(numX, numY)
