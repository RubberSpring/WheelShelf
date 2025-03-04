from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from utils import pathwrap, ButtonLineEdit

from pathlib import Path
import sqlite3
import json
import os


class CollectionManager(QtWidgets.QDialog):
    def delete_collection(self, name):
        for collection in self.data["collections"]:
            if collection["name"] == name:
                self.data["collections"].remove(collection)
                with open(pathwrap("./config/collections.json"), "w") as f:
                    f.write(json.dumps(self.data))

    def export_collection(self, name):
        for collection in self.data["collections"]:
            if collection["name"] == name:
                file = QtWidgets.QFileDialog.getSaveFileName(self)
                print(file)

    def __init__(self, window):
        super().__init__()

        with open(pathwrap("./config/collections.json"), "r") as f:
            self.data = json.load(f)

        def getitem(item):
            global name
            name = item.text()

        collection_list = QtWidgets.QListWidget()
        collection_list.itemClicked.connect(getitem)

        for collection in self.data["collections"]:
            collection_list.addItem(collection["name"])

        open_button = QtWidgets.QPushButton("Open")
        open_button.clicked.connect(window.loadCollection(name))

        delete_button = QtWidgets.QPushButton("Delete")
        open_button.clicked.connect(self.delete_collection(name))

        export_button = QtWidgets.QPushButton("Export")
        export_button.clicked.connect(self.export_collection(name))

        main_layout = QtWidgets.QHBoxLayout()
        buttons_layout = QtWidgets.QVBoxLayout()

        buttons_layout.addWidget(open_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(export_button)

        main_layout.addWidget(collection_list)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)


class NewCollection(QtWidgets.QDialog):
    def __init__(self, window):
        super().__init__()

        self.parent_win = window

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
            f"Collection will be created at\n{path}",
            buttons=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
            defaultButton=QtWidgets.QMessageBox.Cancel,
        )
        if dialog == QtWidgets.QMessageBox.Ok:
            try:
                Path(path).mkdir(parents=True)
            except FileExistsError:
                name = self.name_input.text()
                err = QtWidgets.QMessageBox.critical(
                    self,
                    "Failed",
                    f"Failed to create Collection, a folder named {name} already exists",
                )
                if err == QtWidgets.QMessageBox.Ok:
                    return None

            conn = sqlite3.connect(Path(path, "collection.db"))
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE "cars" (
	                        "image"	TEXT,
	                        "model-name"	TEXT,
	                        "release-year"	TEXT,
	                        "series"	TEXT,
	                        "color"	TEXT,
	                        "wheel-type"	TEXT,
	                        "base-type"	TEXT,
	                        "base-color"	TEXT,
	                        "window-color"	TEXT,
	                        "interior-color"	TEXT,
	                        "toy-num"	TEXT,
	                        "assortment-num"	TEXT,
	                        "scale"	TEXT,
	                        "country"	TEXT
                            );"""
            )
            conn.commit()
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

            if not os.path.exists(pathwrap("./config/collections.json")):
                file = Path("./config/collections.json")
                file.parent.mkdir(exist_ok=True, parents=True)
                with open(pathwrap("./config/collections.json"), "w") as f:
                    info = {
                        "collections": [{"name": self.name_input.text(), "path": path}]
                    }
                    f.write(json.dumps(info))
            else:
                with open(pathwrap("./config/collections.json"), "r+") as f:
                    info = f.read()
                    info["collections"].append(
                        {"name": self.name_input.text(), "path": path}
                    )
                    f.write(json.dumps(info))

            done = QtWidgets.QMessageBox.information(
                self,
                "Done!",
                "Finished creating collection.",
                buttons=QtWidgets.QMessageBox.Ok,
            )
            if done == QtWidgets.QMessageBox.Ok:
                self.parent_win.close()
                self.close()
