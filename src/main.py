from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
import pandas as pd

from pathlib import Path

def pathwrap(path):
    return str(Path(path))

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WheelShelf")
        self.setMinimumSize(QtCore.QSize(800, 500))

        toolbar = QtWidgets.QToolBar("Tools")
        self.addToolBar(toolbar)

        # Import and Export buttons
        import_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/document-import.png")), "Import", self)
        import_action.setStatusTip("Imports cars from a file.")

        export_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/document-export.png")), "Export", self)
        export_action.setStatusTip("Exports the open collection to a file.")

        # Undo and Redo buttons
        undo_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/arrow-curve-180.png")), "Undo", self)
        undo_action.setStatusTip("Undoes the latest action.")
        undo_action.setShortcut(QtGui.QKeySequence("Ctrl+z"))

        redo_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/arrow-curve.png")), "Redo", self)
        redo_action.setStatusTip("Redoes the latest undo.")
        redo_action.setShortcut(QtGui.QKeySequence("Ctrl+y"))

        # Clipboard buttons
        cut_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/scissors.png")), "Cut", self)
        cut_action.setStatusTip("Copies the selected car to the clipboard and removes it.")
        cut_action.setShortcut(QtGui.QKeySequence("Ctrl+x"))

        copy_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/document-copy.png")), "Copy", self)
        copy_action.setStatusTip("Copies the selected car to the clipboard.")
        copy_action.setShortcut(QtGui.QKeySequence("Ctrl+c"))

        paste_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/clipboard.png")), "Paste", self)
        paste_action.setStatusTip("Pastes a car from the clipboard.")
        paste_action.setShortcut(QtGui.QKeySequence("Ctrl+c"))

        # Car buttons
        add_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/car--plus.png")), "Add Cars", self)
        add_action.setStatusTip("Adds a car to the collection.")
        add_action.setShortcut(QtGui.QKeySequence("Ins"))

        remove_action = QtGui.QAction(QtGui.QIcon(pathwrap("./icons/car--minus.png")), "Remove Cars", self)
        remove_action.setStatusTip("Removes a car from the collection.")
        remove_action.setShortcut(QtGui.QKeySequence("Del"))
        
        toolbar.addAction(import_action)
        toolbar.addAction(export_action)

        toolbar.addSeparator()
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)

        toolbar.addSeparator()
        toolbar.addAction(cut_action)
        toolbar.addAction(copy_action)
        toolbar.addAction(paste_action)

        toolbar.addSeparator()
        toolbar.addAction(add_action)
        toolbar.addAction(remove_action)

        toolbar.setMovable(False)

        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
            [1,2,3],
            [23,46,123],
        ], columns=["a","b","c"], index=["1","2"])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        mainlayout = QtWidgets.QHBoxLayout()
        sidelayout = QtWidgets.QVBoxLayout()

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
