from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

from utils import pathwrap, ButtonLineEdit

from pathlib import Path
import sqlite3
import shutil
import json
import os


class NewCollection(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        title = QtWidgets.QLabel("This wizard will create a new WheelShelf collection")
        title_font = title.font()
        title_font.setPointSize(13)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        desc = QtWidgets.QLabel("A collection is where all your cars are stored.")

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("The name of your collection")

        self.path_input = ButtonLineEdit(pathwrap("./icons/folder--arrow.png"))
        self.path_input.setPlaceholderText("The path for your collection")
        self.path_input.buttonClicked.connect(self.selectPath)

        form = QtWidgets.QFormLayout()
        form.addRow("Name:", self.name_input)
        form.addRow("Path:", self.path_input)

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.createCollection)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(desc)
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def selectPath(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()
        self.path_input.setText(directory)

    def createCollection(self):
        path = str(Path(self.path_input.text(), self.name_input.text()))
        dialog = QtWidgets.QMessageBox.question(
            self,
            "Confirm Collection",
            "Collection will be created at\n%s" % path,
            buttons=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
            defaultButton=QtWidgets.QMessageBox.Cancel,
        )
        if dialog == QtWidgets.QMessageBox.Ok:

            try:
                Path(path).mkdir(parents=True)
            except FileExistsError:
                err = QtWidgets.QMessageBox.critical(
                    self, "Failed", "Failed to create Collection, a folder named %s already exists" % self.name_input.text()
                )
                if err == QtWidgets.QMessageBox.Ok:
                    return None

            conn = sqlite3.connect(Path(path, "collection.db"))
            conn.close()
            if not os.path.exists(Path(path, "collection.db")):
                QtWidgets.QMessageBox.critical(
                    self, "Failed", "Failed to create Collection"
                )

            data = {"name": self.name_input.text()}

            with open(Path(path, "info.json"), "w") as f:
                f.write(json.dumps(data))

            if not os.path.exists(Path(path, "info.json")):
                QtWidgets.QMessageBox.critical(
                    self, "Failed", "Failed to create Collection"
                )

            done = QtWidgets.QMessageBox.information(
                self,
                "Done!",
                "Finished creating collection.",
                buttons=QtWidgets.QMessageBox.Ok
            )
            if done == QtWidgets.QMessageBox.Ok:
                self.close()
            