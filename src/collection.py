from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

from utils import pathwrap, ButtonLineEdit

class NewCollection(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        title = QtWidgets.QLabel("This wizard will create a new WheelShelf collection")
        title_font = title.font()
        title_font.setPointSize(13)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        desc = QtWidgets.QLabel("A collection is where all your cars are stored.")

        name_input = QtWidgets.QLineEdit()
        name_input.setPlaceholderText("The name of your collection")

        self.path_input = ButtonLineEdit(pathwrap("./icons/folder--arrow.png"))
        self.path_input.setPlaceholderText("The path for your collection")
        self.path_input.buttonClicked.connect(self.selectPath)

        form = QtWidgets.QFormLayout()
        form.addRow("Name:", name_input)
        form.addRow("Path:", self.path_input)

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(buttons)
        button_box.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(desc)
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def selectPath(self):
        directory = QtWidgets.QFileDialog.Get
        self.path_input.setText(directory)