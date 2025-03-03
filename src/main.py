from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

import pandas as pd

import sys
import os

from utils import pathwrap, error_hook, TableModel
from collection import NewCollection

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        sys.excepthook = error_hook

        self.setWindowTitle("WheelShelf")
        self.setMinimumSize(QtCore.QSize(800, 500))

        toolbar = QtWidgets.QToolBar("Tools")
        self.addToolBar(toolbar)

        # Import and Export buttons
        import_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/document-import.png")), "Import", self
        )
        import_action.setStatusTip("Imports cars from a file.")

        export_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/document-export.png")), "Export", self
        )
        export_action.setStatusTip("Exports the open collection to a file.")

        # Undo and Redo buttons
        undo_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/arrow-curve-180.png")), "Undo", self
        )
        undo_action.setStatusTip("Undoes the latest action.")
        undo_action.setShortcut(QtGui.QKeySequence("Ctrl+z"))

        redo_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/arrow-curve.png")), "Redo", self
        )
        redo_action.setStatusTip("Redoes the latest undo.")
        redo_action.setShortcut(QtGui.QKeySequence("Ctrl+y"))

        # Clipboard buttons
        cut_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/scissors.png")), "Cut", self
        )
        cut_action.setStatusTip(
            "Copies the selected car to the clipboard and removes it."
        )
        cut_action.setShortcut(QtGui.QKeySequence("Ctrl+x"))

        copy_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/document-copy.png")), "Copy", self
        )
        copy_action.setStatusTip("Copies the selected car to the clipboard.")
        copy_action.setShortcut(QtGui.QKeySequence("Ctrl+c"))

        paste_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/clipboard.png")), "Paste", self
        )
        paste_action.setStatusTip("Pastes a car from the clipboard.")
        paste_action.setShortcut(QtGui.QKeySequence("Ctrl+c"))

        # Car buttons
        add_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/car--plus.png")), "Add Cars", self
        )
        add_action.setStatusTip("Adds a car to the collection.")
        add_action.setShortcut(QtGui.QKeySequence("Ins"))

        remove_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/car--minus.png")), "Remove Cars", self
        )
        remove_action.setStatusTip("Removes a car from the collection.")
        remove_action.setShortcut(QtGui.QKeySequence("Del"))

        collection_action = QtGui.QAction(
            QtGui.QIcon(pathwrap("./icons/books-stack")), "Change Collection", self
        )
        collection_action.setStatusTip("Changes the active collection.")

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )

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

        toolbar.addWidget(spacer)
        toolbar.addAction(collection_action)

        toolbar.setMovable(False)

        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame(
            [],
            columns=["Image", "Model Name", "Toy Number", "Series", "Color", "Price"],
            index=[],
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)

        if not os.path.exists(pathwrap("./config/collections.json")):
            dialog = GreetingWindow()
            dialog.setWindowTitle("Welcome!")
            dialog.exec()

        main_layout = QtWidgets.QHBoxLayout()
        side_layout = QtWidgets.QVBoxLayout()
        image_layout = QtWidgets.QVBoxLayout()
        info_layout = QtWidgets.QVBoxLayout()


class GreetingWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        sys.excepthook = error_hook

        self.setFixedSize(QtCore.QSize(600, 350))

        banner = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(pathwrap("./icons/wheelshelf_banner.png"))
        banner.setPixmap(pixmap)

        title = QtWidgets.QLabel("Welcome to WheelShelf!")
        title_font = title.font()
        title_font.setPointSize(20)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        desc = QtWidgets.QLabel(
            "WheelShelf is a powerful Hot Wheels\ncollection management software for PC."
        )
        desc_font = desc.font()
        desc_font.setPointSize(14)
        desc.setFont(desc_font)

        help = QtWidgets.QLabel("Create or open a existent collection")
        help_font = help.font()
        help_font.setPointSize(10)
        help.setFont(help_font)
        help.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        new_btn = QtWidgets.QPushButton("New Collection")
        new_btn.clicked.connect(self.new_collection)

        import_btn = QtWidgets.QPushButton("Import Collection file")

        open_btn = QtWidgets.QPushButton("Open collection from folder")

        buttons = QtWidgets.QVBoxLayout()
        buttons.addWidget(new_btn)
        buttons.addWidget(import_btn)
        buttons.addWidget(open_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(banner, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(desc)
        layout.addSpacing(10)
        layout.addWidget(help)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def new_collection(self):
        dialog = NewCollection(self)
        dialog.setWindowTitle("New Collection")
        dialog.exec()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
