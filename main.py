import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image')
        self.setGeometry(500, 200, 500, 500)

        but = QPushButton(self)
        but.setIcon(QIcon('settings.jpg'))
        but.setIconSize(QSize(20, 20))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
