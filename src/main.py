from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow
)

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WheelShelf")

        self.setMinimumSize(QSize(800, 500))

window = MainWindow()
window.show()

app.exec()