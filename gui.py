from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 1280, 720)
    win.setWindowTitle("DayZ ModLauncher")
    
    win.show()
    sys.exit(app.exec())

window()