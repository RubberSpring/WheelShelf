from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

from pathlib import Path
from sys import exit


def pathwrap(path):
    return str(Path(path))


class DebugDialog(QtWidgets.QDialog):
    def __init__(self, exc_type, exc_value, exc_tb):
        super().__init__()

        title = QtWidgets.QLabel(
            "This is development debug data.\nIf you came from an error message, remember to post this debug data when opening a issue."
        )

        debug = QtWidgets.QPlainTextEdit(f"{exc_tb}\n{exc_type}:\n{exc_value}")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(debug)


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


class ButtonLineEdit(QtWidgets.QLineEdit):
    buttonClicked = QtCore.Signal()

    def __init__(self, icon_file, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QtWidgets.QToolButton(self)
        self.button.setIcon(QtGui.QIcon(icon_file))
        self.button.setStyleSheet("border: 0px; padding: 0px;")
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet(
            "QLineEdit {padding-right: %dpx; }" % (buttonSize.width() + frameWidth + 1)
        )
        self.setMinimumSize(
            max(
                self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2
            ),
            max(
                self.minimumSizeHint().height(),
                buttonSize.height() + frameWidth * 2 + 2,
            ),
        )

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - frameWidth - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )
        super(ButtonLineEdit, self).resizeEvent(event)
