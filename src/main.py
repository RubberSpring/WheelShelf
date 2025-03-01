from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
import pandas as pd

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

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
            [1,2,3],
            [23,46,123],
        ], columns=["a","b","c"], index=["1","2"])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
