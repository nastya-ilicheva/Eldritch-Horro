import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 500)
        self.setWindowTitle('eBook')

    def initUI(self):
        self.setWindowTitle('eBook')
        # self.setGeometry(500, 200)


class Buttons(Main, QWidget):
    def initUI(self):
        self.settings_but = QPushButton(self)
        self.settings_but.setIcon(QIcon('settings.png'))
        self.settings_but.setIconSize(QSize(20, 20))
        self.settings_but.move(470, 0)

        self.settings_but = QPushButton(self)
        self.settings_but.setIcon(QIcon('three_points.png'))
        self.settings_but.setIconSize(QSize(20, 20))
        self.settings_but.move(0, 0)

        self.title = QLabel(self)
        self.title.setFixedSize(150, 20)
        self.title.move(200, 0)
        self.title.setText("fz")

        self.show()



        # settings_menu = QMenu(self)
        # сделать меню(выпадающий список)


# class Title(Main, QWidget):
#     def initUI(self):
#         self.title = QTextBrowser()
#         self.title.setFixedSize(150, 20)
#         self.title.move(20, 0)
#         self.show()


# class MoreFunction(Main, QWidget):
#     def initUI(self):
#         self.settings_but = QPushButton(self)
#         self.settings_but.setIcon(QIcon('three_points.png'))
#         self.settings_but.setIconSize(QSize(20, 20))
#         self.settings_but.move(0, 0)
#         self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    e = Buttons()
    # x = MoreFunction()
    sys.exit(app.exec_())
