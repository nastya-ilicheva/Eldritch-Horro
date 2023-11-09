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

        self.three_points = QPushButton(self)
        self.three_points.setIcon(QIcon('three_points.png'))
        self.three_points.setIconSize(QSize(20, 20))
        self.three_points.move(0, 0)

        self.title = QLabel(self)
        self.title.setFixedSize(150, 20)
        self.title.move(200, 0)
        self.title.setText("fz")

        self.show()

        # Создаем контекстное меню
        # создфть еще 3 кнопки
        context_menu = QMenu(self.three_points)
        action_book_description = QAction("book description", context_menu)
        action_table_of_contents = QAction("table of contents", context_menu)
        action_bookmarks = QAction("bookmarks", context_menu)
        action_tp_to_the_page = QAction("go to the page", context_menu)
        action_read = QAction("read", context_menu)

        # Присоединяем действия к соответствующим функциям
        action_book_description.triggered.connect(self.action_book_description)
        action_table_of_contents.triggered.connect(self.action_table_of_contents)
        action_table_of_contents.triggered.connect(self.action_bookmarks)
        action_table_of_contents.triggered.connect(self.action_tp_to_the_page)
        action_table_of_contents.triggered.connect(self.action_read)

        # Добавляем пункты меню к контекстному меню
        context_menu.addAction(action_book_description)
        context_menu.addAction(action_table_of_contents)
        context_menu.addAction(action_bookmarks)
        context_menu.addAction(action_tp_to_the_page)
        context_menu.addAction(action_read)

        # Прикрепляем контекстное меню к кнопке
        self.three_points.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.three_points.customContextMenuRequested.connect(lambda pos: context_menu.exec_(self.three_points.mapToGlobal(pos)))

    def action_book_description(self):
        # self.three_points.setStyleSheet("background-color: red;")
        pass

    def action_table_of_contents(self):
        # self.three_points.setStyleSheet("background-color: green;")
        pass

    def action_bookmarks(self):
        pass

    def action_tp_to_the_page(self):
        pass

    def action_read(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    e = Buttons()
    # x = MoreFunction()
    sys.exit(app.exec_())
