import os
import FreeCAD
from PySide import QtGui, QtCore

EXPORTABLE_PREFIXES = ("GFPlus_Bin_", "GFPlus_Baseplate_")


class BulkExportTaskPanel:
    def __init__(self, command):
        self.command = command
        self.form = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()

        # Folder selection
        folder_layout = QtGui.QHBoxLayout()
        self.folderEdit = QtGui.QLineEdit()
        self.folderEdit.setPlaceholderText("Select export folder...")
        self.browseButton = QtGui.QPushButton("Browse...")
        self.browseButton.clicked.connect(self._browse_folder)
        folder_layout.addWidget(self.folderEdit)
        folder_layout.addWidget(self.browseButton)
        layout.addLayout(folder_layout)

        # Object list
        layout.addWidget(QtGui.QLabel("Objects to export:"))
        self.objectList = QtGui.QListWidget()
        self.objectList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self._populate_objects()
        layout.addWidget(self.objectList)

        # Select all / none buttons
        sel_layout = QtGui.QHBoxLayout()
        selectAllBtn = QtGui.QPushButton("Select All")
        selectAllBtn.clicked.connect(self._select_all)
        selectNoneBtn = QtGui.QPushButton("Select None")
        selectNoneBtn.clicked.connect(self._select_none)
        sel_layout.addWidget(selectAllBtn)
        sel_layout.addWidget(selectNoneBtn)
        layout.addLayout(sel_layout)

        # Format selection
        fmt_layout = QtGui.QHBoxLayout()
        fmt_layout.addWidget(QtGui.QLabel("Format:"))
        self.formatCombo = QtGui.QComboBox()
        self.formatCombo.addItems(["STL", "STEP", "Both"])
        fmt_layout.addWidget(self.formatCombo)
        layout.addLayout(fmt_layout)

        # Export button
        self.exportButton = QtGui.QPushButton("Export")
        self.exportButton.clicked.connect(self._on_export)
        layout.addWidget(self.exportButton)

        self.form.setLayout(layout)

    def _populate_objects(self):
        self.objectList.clear()
        doc = FreeCAD.ActiveDocument
        if not doc:
            return
        for obj in doc.Objects:
            if any(obj.Name.startswith(p) for p in EXPORTABLE_PREFIXES):
                item = QtGui.QListWidgetItem(obj.Name)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
                self.objectList.addItem(item)

    def _browse_folder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self.form, "Select Export Folder")
        if folder:
            self.folderEdit.setText(folder)

    def _select_all(self):
        for i in range(self.objectList.count()):
            self.objectList.item(i).setCheckState(QtCore.Qt.Checked)

    def _select_none(self):
        for i in range(self.objectList.count()):
            self.objectList.item(i).setCheckState(QtCore.Qt.Unchecked)

    def _on_export(self):
        folder = self.folderEdit.text().strip()
        if not folder:
            QtGui.QMessageBox.warning(self.form, "No Folder", "Please select an export folder.")
            return
        if not os.path.isdir(folder):
            QtGui.QMessageBox.warning(self.form, "Invalid Folder", f"Folder does not exist: {folder}")
            return

        selected_names = [
            self.objectList.item(i).text()
            for i in range(self.objectList.count())
            if self.objectList.item(i).checkState() == QtCore.Qt.Checked
        ]

        if not selected_names:
            QtGui.QMessageBox.warning(self.form, "Nothing Selected", "Please select at least one object to export.")
            return

        doc = FreeCAD.ActiveDocument
        objects = [doc.getObject(n) for n in selected_names if doc.getObject(n)]
        fmt = self.formatCombo.currentText()

        exported, failed = self.command.ExportObjects(objects, folder, fmt)

        msg = f"Exported {len(exported)} object(s) to:\n{folder}"
        if failed:
            msg += f"\n\nFailed: {', '.join(failed)}"
        QtGui.QMessageBox.information(self.form, "Export Complete", msg)
