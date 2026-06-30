import FreeCAD
from PySide import QtGui, QtCore


class BinTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()

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

        self.numXMinInput.valueChanged.connect(self.onXMinValueChanged)
        self.numXMaxInput.valueChanged.connect(self.onXMaxValueChanged)
        self.numYMinInput.valueChanged.connect(self.onYMinValueChanged)
        self.numYMaxInput.valueChanged.connect(self.onYMaxValueChanged)

        self.labelEnum = QtGui.QLabel("Selection:")
        self.layout.addWidget(self.labelEnum)
        self.enumInput = QtGui.QComboBox()
        self.enumInput.addItems(["edges", "corners", "fill", "none"])
        self.layout.addWidget(self.enumInput)

        self.labelHeight = QtGui.QLabel("Heights (comma-separated):")
        self.layout.addWidget(self.labelHeight)
        self.heightInput = QtGui.QLineEdit()
        self.heightInput.setPlaceholderText("0.75, 1.5, 2.25")
        self.heightInput.setText("0.75, 1.25")
        self.layout.addWidget(self.heightInput)

        self.createButton = QtGui.QPushButton("Create Bin")
        self.createButton.clicked.connect(self.CreateBin)
        self.layout.addWidget(self.createButton)

        self.form.setLayout(self.layout)

    def onXMinValueChanged(self, value):
        if value > self.numXMaxInput.value():
            self.numXMaxInput.setValue(value)

    def onXMaxValueChanged(self, value):
        if value < self.numXMinInput.value():
            self.numXMinInput.setValue(value)

    def onYMinValueChanged(self, value):
        if value > self.numYMaxInput.value():
            self.numYMaxInput.setValue(value)

    def onYMaxValueChanged(self, value):
        if value < self.numYMinInput.value():
            self.numYMinInput.setValue(value)

    def parse_heights(self):
        height_str = self.heightInput.text()
        try:
            heights = [float(h.strip()) for h in height_str.split(',')]
            return [h for h in heights if 0 <= h <= 359]
        except ValueError:
            QtGui.QMessageBox.warning(None, "Invalid Input", "Please enter valid comma-separated numbers for heights.")
            return []

    def bin_exists(self, NumX, NumY, Height, selection):
        doc = FreeCAD.ActiveDocument
        if not doc:
            return False
        bin_name = f"GFPlus_Bin_{NumX}x{NumY}x{Height:.2f}_{selection}".replace('.', '_')
        return bin_name in [obj.Name for obj in doc.Objects]

    def CreateBin(self):
        numXMin = self.numXMinInput.value()
        numXMax = self.numXMaxInput.value()
        numYMin = self.numYMinInput.value()
        numYMax = self.numYMaxInput.value()
        selection = self.enumInput.currentText()
        heights = self.parse_heights()

        if not heights:
            return

        for numX in range(numXMin, numXMax + 1):
            for numY in range(numYMin, numYMax + 1):
                for height in heights:
                    if not self.bin_exists(numX, numY, height, selection):
                        self.command.CreateBin(numX, numY, selection, height)
                    else:
                        FreeCAD.Console.PrintMessage(f"[GFPlus] BinTaskPanel.CreateBin: bin {numX}x{numY}x{height:.2f} '{selection}' already exists, skipping\n")
