import sys
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from bookmarks_db import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 500)
        self.setWindowTitle('eBook')


    def resizeEvent(self, event):
        self.text_lable.setGeometry(0, sum([b.height() for b in [self.three_points, self.title]]),
                                   event.size().width(), event.size().height() - sum(
                [b.height() for b in [self.three_points, self.title]]))

    def initUI(self):
        self.three_points = QPushButton(self)
        self.title = QLabel(self)
        self.text_lable = QTextEdit(self)

        self.three_points.setIcon(QIcon('system_files/three_points.png'))
        self.three_points.setIconSize(QSize(20, 20))
        self.three_points.move(0, 0)

        self.title.setFixedSize(460, 20)
        self.title.move(40, 0)
        self.title.setText("")

        self.text_lable.setText("Выберите книгу из библиотеки")
        self.f = self.text_lable.font()
        self.f.setPointSize(14)  # sets the size to 27
        self.text_lable.setFont(self.f)
        self.text_lable.setReadOnly(True)

        layout_cap = QVBoxLayout()
        # layout_cap.addWidget(self.settings)
        layout_cap.addWidget(self.three_points)
        layout_cap.addWidget(self.title)

        layout = QVBoxLayout()
        layout.addLayout(layout_cap)
        layout.addWidget(self.text_lable)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

        # Создаем контекстное меню для 3точки
        context_menu_three_point = QMenu(self.three_points)
        action_table_of_contents = QAction("оглавление", context_menu_three_point)
        action_bookmarks = QAction("заметки", context_menu_three_point)
        action_read = QAction("аудиокнига", context_menu_three_point)
        action_library = QAction("библиотека", context_menu_three_point)
        action_file_selection = QAction("добавление файла", context_menu_three_point)

        action_font_size = QAction("размер шрифта", context_menu_three_point)
        action_help = QAction("помощь", context_menu_three_point)
        action_color = QAction("цвет", context_menu_three_point)
        action_font = QAction("редактировать отображение текста", context_menu_three_point)
        action_about_the_program = QAction("о программе", context_menu_three_point)

        action_table_of_contents.triggered.connect(self.action_table_of_contents)
        action_bookmarks.triggered.connect(self.action_bookmarks)
        action_read.triggered.connect(self.action_read)
        action_library.triggered.connect(self.action_library)
        action_file_selection.triggered.connect(self.action_file_selection)

        action_font_size.triggered.connect(self.action_font_size)
        action_help.triggered.connect(self.action_help)
        action_font.triggered.connect(self.action_font)
        action_color.triggered.connect(self.action_color)
        action_about_the_program.triggered.connect(self.action_about_the_program)

        context_menu_three_point.addAction(action_table_of_contents)
        context_menu_three_point.addAction(action_bookmarks)
        context_menu_three_point.addAction(action_read)
        context_menu_three_point.addAction(action_library)
        context_menu_three_point.addAction(action_file_selection)

        context_menu_three_point.addAction(action_font_size)
        context_menu_three_point.addAction(action_help)
        context_menu_three_point.addAction(action_font)
        context_menu_three_point.addAction(action_color)
        context_menu_three_point.addAction(action_about_the_program)

        self.three_points.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.three_points.customContextMenuRequested.connect(
            lambda pos: context_menu_three_point.exec_(self.three_points.mapToGlobal(pos)))

    def action_table_of_contents(self):
        QMessageBox.about(self, "Оглавление", "Эта фукнция пока не реализована)")

    def action_bookmarks(self):
        self.ex = BookmarksDB()
        self.ex.show()

    def action_read(self):
        QMessageBox.about(self, "Аудиокнига", "Эта фукнция пока не реализована)")

    def action_library(self):
        f = open("system_files/library.txt", 'r')
        library = f.readlines()
        f.close()

        book_name, ok_pressed = QInputDialog.getItem(
            self, "file", "choose book",
            tuple(library), 1, False)

        self.boasasoa = book_name  # без него не рабоатет

        self.f.setPointSize(10)
        self.text_lable.setFont(self.f)
        self.title.setText(book_name[:-1])

        if ok_pressed:
            try:
                self.text_lable.clear()
                with io.open(book_name[:-1], encoding='utf-8') as file:
                    for i in file:
                        self.text_lable.append(i)
            except Exception as e:
                print(e)

    def action_file_selection(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'open file', '',
            'book (*.txt)')[0]
        # self.library.append(self.fname)

        f = open("system_files/library.txt", 'a')
        print(f.write(f"{self.fname}\n"))
        f.close()

        QMessageBox.about(self, "Title", "Файл добавлен в библиотеку")

    def action_font_size(self):
        try:
            size, ok_pressed = QInputDialog.getInt(
                self, "Шрифт", "Выберите размер шрифта",
                10, 1, 35, 1)
            if ok_pressed:
                self.f.setPointSize(size)
                self.text_lable.setFont(self.f)
                with io.open(self.boasasoa[:-1], encoding='utf-8') as file:
                    for i in file:
                        self.text_lable.append(i)
        except Exception as e:
            print(e)

    def action_help(self):
        QMessageBox.about(self, "Помощь", "Сверху есть панель инструментов. В двух кнопках(3_точки и "
                                          "настройки) спрятаны различные функции. Чтоб приступить к чтению книги, "
                                          "необходимо добавить ее в библиотеку, после открыть. Есть возможность "
                                          "добавления цитат, различных заметок, описания книг. Приятного чтения!")

    def action_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_lable.setFont(font)

    def action_color(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.text_lable.setStyleSheet("QWidget { background-color: %s }"
                                          % col.name())

    def action_about_the_program(self):
        QMessageBox.about(self, "eBook", "eBook - компьютерная программа для чтения электронных книг в "
                                         "формате txt. В графическом интерфейсе программы есть панель инструментов с "
                                         "кнопками и названием, читаемой книги,есть возможность подстроить интерфейс "
                                         "подстроить под себя.")

    def closeEvent(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
