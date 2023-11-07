import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 500)


    def initUI(self):
        self.setWindowTitle('eBook')
        # self.setGeometry(500, 200)



class Settings(Main, QWidget):
    def initUI(self):
        settings_but = QPushButton(self)
        settings_but.setIcon(QIcon('settings.png'))
        settings_but.setIconSize(QSize(20, 20))
        self.show()

        settings_menu = QMenu(self)
        # сделать меню(выпадающий список)


class Title(Main, QWidget):
    pass


class MoreFunction(Main, QWidget):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    e = Settings()
    sys.exit(app.exec_())
