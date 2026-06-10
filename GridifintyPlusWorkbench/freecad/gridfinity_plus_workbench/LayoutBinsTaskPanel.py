import re
import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

CELL_SIZE = 60  # pixels per grid cell

BIN_COLORS = [
    QtGui.QColor(100, 160, 240),
    QtGui.QColor(90, 200, 130),
    QtGui.QColor(240, 160, 80),
    QtGui.QColor(200, 100, 200),
    QtGui.QColor(240, 200, 80),
    QtGui.QColor(80, 200, 220),
]


def _parse_bin_dimensions(bin_name):
    match = re.match(r'GFPlus_Bin_(\d+)x(\d+)', bin_name)
    if match:
        return int(match.group(1)), int(match.group(2))
    FreeCAD.Console.PrintWarning(f"[GFPlus] LayoutBins: cannot parse dimensions from '{bin_name}', using 1x1.\n")
    return 1, 1


def _detect_bins():
    doc = FreeCAD.ActiveDocument
    if not doc:
        return []
    names = [obj.Name for obj in doc.Objects if obj.Name.startswith("GFPlus_Bin_")]
    names.sort(key=_parse_bin_dimensions)
    return names


def _detect_baseplate():
    doc = FreeCAD.ActiveDocument
    if not doc:
        return None
    for obj in doc.Objects:
        if obj.Name.startswith("GFPlus_Baseplate_"):
            parts = obj.Name.split("_")
            try:
                return int(parts[2]), int(parts[3])
            except (IndexError, ValueError):
                continue
    return None


# ---------------------------------------------------------------------------
# BinItem — a placed bin tile on the grid
# ---------------------------------------------------------------------------

class BinItem(QtGui.QGraphicsRectItem):
    def __init__(self, bin_name, numX, numY, gx, gy, cell_size, scene_ref, color):
        # 1-px inset so grid lines remain visible between adjacent bins
        super().__init__(1, 1, numX * cell_size - 2, numY * cell_size - 2)
        self.bin_name = bin_name
        self.numX = numX
        self.numY = numY
        self.gx = gx
        self.gy = gy
        self.cell_size = cell_size
        self.scene_ref = scene_ref

        self.setPos(gx * cell_size, gy * cell_size)
        self.setBrush(QtGui.QBrush(color))
        self.setPen(QtGui.QPen(QtGui.QColor(40, 40, 40), 1))
        self.setFlags(
            QtGui.QGraphicsItem.ItemIsMovable |
            QtGui.QGraphicsItem.ItemIsSelectable |
            QtGui.QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setZValue(1)
        self.setToolTip(bin_name)

        label = QtGui.QGraphicsTextItem(bin_name.replace('GFPlus_Bin_', ''), self)
        label.setPos(4, 4)
        label.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        font = QtGui.QFont()
        font.setPointSize(7)
        label.setFont(font)

    def mouseReleaseEvent(self, event):
        pos = self.pos()
        cell = self.cell_size
        # Remove if dragged so the bin's center exits the grid
        cx = pos.x() + self.numX * cell / 2
        cy = pos.y() + self.numY * cell / 2
        scene_w = self.scene_ref.baseplate_x * cell
        scene_h = self.scene_ref.baseplate_y * cell
        if cx < 0 or cy < 0 or cx > scene_w or cy > scene_h:
            super().mouseReleaseEvent(event)
            QtCore.QTimer.singleShot(0, lambda: self.scene_ref.remove_bin(self))
            return
        new_gx = round(pos.x() / cell)
        new_gy = round(pos.y() / cell)
        new_gx = max(0, min(new_gx, self.scene_ref.baseplate_x - self.numX))
        new_gy = max(0, min(new_gy, self.scene_ref.baseplate_y - self.numY))
        moved = self.scene_ref.can_place(self, new_gx, new_gy)
        if moved:
            self.gx = new_gx
            self.gy = new_gy
        self.setPos(self.gx * cell, self.gy * cell)
        super().mouseReleaseEvent(event)
        if moved:
            self.scene_ref.layout_changed.emit()


# ---------------------------------------------------------------------------
# BaseplateScene — QGraphicsScene that owns the grid and placed bins
# ---------------------------------------------------------------------------

class BaseplateScene(QtGui.QGraphicsScene):
    layout_changed = QtCore.Signal()

    def __init__(self, baseplate_x, baseplate_y, cell_size=CELL_SIZE):
        super().__init__()
        self.baseplate_x = baseplate_x
        self.baseplate_y = baseplate_y
        self.cell_size = cell_size
        self.bin_items = []
        self._color_map = {}
        self._next_color = 0
        self._draw_grid()

    def _draw_grid(self):
        cell = self.cell_size
        bg_pen = QtGui.QPen(QtGui.QColor(130, 130, 130), 1)
        cell_brush = QtGui.QBrush(QtGui.QColor(230, 230, 230))
        for x in range(self.baseplate_x):
            for y in range(self.baseplate_y):
                r = self.addRect(x * cell, y * cell, cell, cell, bg_pen, cell_brush)
                r.setZValue(-1)

    def _get_color(self, bin_name):
        if bin_name not in self._color_map:
            self._color_map[bin_name] = BIN_COLORS[self._next_color % len(BIN_COLORS)]
            self._next_color += 1
        return self._color_map[bin_name]

    def can_place(self, exclude_item, gx, gy):
        """Return True if exclude_item can be placed at (gx, gy) without overlapping others."""
        numX, numY = exclude_item.numX, exclude_item.numY
        cells = {(gx + dx, gy + dy) for dx in range(numX) for dy in range(numY)}
        for item in self.bin_items:
            if item is exclude_item:
                continue
            occupied = {(item.gx + dx, item.gy + dy)
                        for dx in range(item.numX) for dy in range(item.numY)}
            if cells & occupied:
                return False
        return True

    def add_bin(self, bin_name, numX, numY, gx, gy):
        """Place a new bin. Returns False if out-of-bounds or overlapping."""
        if gx < 0 or gy < 0 or gx + numX > self.baseplate_x or gy + numY > self.baseplate_y:
            return False
        cells = {(gx + dx, gy + dy) for dx in range(numX) for dy in range(numY)}
        for item in self.bin_items:
            occupied = {(item.gx + dx, item.gy + dy)
                        for dx in range(item.numX) for dy in range(item.numY)}
            if cells & occupied:
                return False
        item = BinItem(bin_name, numX, numY, gx, gy, self.cell_size, self, self._get_color(bin_name))
        self.addItem(item)
        self.bin_items.append(item)
        self.layout_changed.emit()
        return True

    def remove_bin(self, item):
        if item in self.bin_items:
            self.removeItem(item)
            self.bin_items.remove(item)
            self.layout_changed.emit()

    def clear_all(self):
        for item in list(self.bin_items):
            self.removeItem(item)
        self.bin_items.clear()
        self.layout_changed.emit()

    def get_entries(self):
        return [{'bin_name': item.bin_name, 'grid_x': item.gx, 'grid_y': item.gy}
                for item in self.bin_items]


# ---------------------------------------------------------------------------
# BaseplateGridView — QGraphicsView that receives drops from the palette
# ---------------------------------------------------------------------------

class BaseplateGridView(QtGui.QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self._scene = scene
        self.setAcceptDrops(True)
        self.setRenderHint(QtGui.QPainter.Antialiasing, False)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasText():
            event.ignore()
            return
        bin_name = event.mimeData().text()
        numX, numY = _parse_bin_dimensions(bin_name)
        scene_pos = self.mapToScene(event.pos())
        gx = int(scene_pos.x() / self._scene.cell_size)
        gy = int(scene_pos.y() / self._scene.cell_size)
        self._scene.add_bin(bin_name, numX, numY, gx, gy)
        event.acceptProposedAction()


# ---------------------------------------------------------------------------
# BinPalette — draggable list of available bins
# ---------------------------------------------------------------------------

class BinPalette(QtGui.QListWidget):
    def __init__(self, bin_names):
        super().__init__()
        self.setDragEnabled(True)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setMaximumHeight(120)
        for name in bin_names:
            short = name.replace('GFPlus_Bin_', '')
            item = QtGui.QListWidgetItem(short)
            item.setData(QtCore.Qt.UserRole, name)
            item.setToolTip(name)
            self.addItem(item)

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if not item:
            return
        bin_name = item.data(QtCore.Qt.UserRole)
        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setText(bin_name)
        drag.setMimeData(mime)
        drag.exec_(QtCore.Qt.CopyAction)


# ---------------------------------------------------------------------------
# LayoutBinsTaskPanel — the FreeCAD task panel
# ---------------------------------------------------------------------------

class LayoutBinsTaskPanel:
    def __init__(self, command):
        self.command = command
        bin_names = _detect_bins()
        baseplate = _detect_baseplate()
        bp_x, bp_y = baseplate if baseplate else (6, 4)

        self._preview_timer = QtCore.QTimer()
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self.update_preview)

        self.form = QtGui.QWidget()
        self.form.setMinimumWidth(max(400, bp_x * CELL_SIZE + 20))
        main_layout = QtGui.QVBoxLayout()

        status = f"Baseplate: {bp_x}x{bp_y}" if baseplate else "No baseplate detected — using 6x4 default grid"
        main_layout.addWidget(QtGui.QLabel(status))

        if not bin_names:
            main_layout.addWidget(QtGui.QLabel("No bins found. Create bins first with Create Bin."))
        else:
            main_layout.addWidget(QtGui.QLabel("Drag bins onto the grid. Drag a placed bin off the grid to remove it."))

        self.palette = BinPalette(bin_names)
        main_layout.addWidget(self.palette)

        self.scene = BaseplateScene(bp_x, bp_y)
        self.scene.layout_changed.connect(self._schedule_preview)

        self.grid_view = BaseplateGridView(self.scene)
        grid_h = min(bp_y * CELL_SIZE + 4, 500)
        self.grid_view.setMinimumHeight(grid_h)
        self.grid_view.setSceneRect(0, 0, bp_x * CELL_SIZE, bp_y * CELL_SIZE)
        main_layout.addWidget(self.grid_view)

        btn_row = QtGui.QHBoxLayout()
        clear_btn = QtGui.QPushButton("Clear All")
        clear_btn.clicked.connect(self.scene.clear_all)
        btn_row.addWidget(clear_btn)
        create_btn = QtGui.QPushButton("Create Layout")
        create_btn.clicked.connect(self.create_layout)
        btn_row.addWidget(create_btn)
        main_layout.addLayout(btn_row)

        self.form.setLayout(main_layout)

    def _schedule_preview(self):
        self._preview_timer.start(250)

    def update_preview(self):
        entries = self.scene.get_entries()
        if entries:
            self.command.PlacePreview(entries)
        else:
            self.command.ClearPreview()

    def accept(self):
        self._preview_timer.stop()
        entries = self.scene.get_entries()
        if entries:
            self.command.PlaceLayout(entries)
        self.command.ClearPreview()

    def reject(self):
        self._preview_timer.stop()
        self.command.ClearPreview()

    def create_layout(self):
        entries = self.scene.get_entries()
        if not entries:
            QtGui.QMessageBox.warning(None, "No Bins", "Place at least one bin on the grid first.")
            return
        self._preview_timer.stop()
        self.command.PlaceLayout(entries)
