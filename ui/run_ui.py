import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from ui.views.main_view import MainView

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()


    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MyMainWindow()

    asd = MainView()
    asd.setupUi(window)
    asd.assign_model()
    window.show()

    sys.exit(app.exec())