import sys
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 500)
        self.setWindowTitle('eBook')

    def initUI(self):
        self.setWindowTitle('eBook')
        e = Buttons()


class StartDialogue(QDialog):
    def __init__(self):
        super(StartDialogue, self).__init__()

        self.answer = QMessageBox.question(
            self,
            'Confirmation',
            'Запустить программу?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        self.check_password_settings()

    def check_password_settings(self):
        if self.answer == QMessageBox.StandardButton.Yes:
            self.ui = Buttons()
            self.close()
        else:
            sys.exit()


class BookmarksDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("bookmarks.ui", self)
        self.con = sqlite3.connect("system_files/ebook.db")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.append_elem)
        self.pushButton_4.clicked.connect(self.delete_elem)

        self.modified = {}
        self.titles = None

    def update_result(self):
        try:
            cur = self.con.cursor()
            if self.spinBox.text() != "0":
                result = cur.execute("SELECT * FROM bookmarks WHERE id=?",
                                     (item_id := self.spinBox.text(),)).fetchall()
                self.tableWidget.setRowCount(len(result))
                # Если запись не нашлась, то не будем ничего делать
                if not result:
                    self.statusBar().showMessage('Ничего не нашлось')
                    return
                else:
                    self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
                self.tableWidget.setColumnCount(len(result[0]))
                self.titles = [description[0] for description in cur.description]
                # Заполнили таблицу полученными элементами
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                self.modified = {}
            else:
                self.cur = self.con.cursor()
                tab1 = "SELECT * FROM bookmarks"
                try:
                    self.statusBar().showMessage('')
                    result = self.cur.execute(tab1).fetchall()
                    self.tableWidget.setRowCount(len(result))
                    self.tableWidget.setColumnCount(len(result[0]))
                    for i, elem in enumerate(result):
                        for j, val in enumerate(elem):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                except Exception as e:
                    print(e)
                self.modified = {}
        except Exception as e:
            print(e)

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM bookmarks WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()

    def append_elem(self):
        self.x = AppendBookmarks()
        self.x.show()
    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE bookmarks SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))

            self.con.commit()
            self.modified.clear()


class AppendBookmarks(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("append_bookmarks.ui", self)
        self.con = sqlite3.connect("system_files/ebook.db")
        self.ok_pressed.clicked.connect(self.remember_result)
        self.cancel_pressed.clicked.connect(self.closes)
        self.modified = {}
        self.titles = None

    def remember_result(self):
        try:
            self.autor = self.author.text()
            self.book_name = self.author.text()
            self.bookmarks = self.bookmarks.text()

            cur = self.con.cursor()
            cur.execute(f"INSERT INTO bookmarks(author, book_name, bookmarks)"
                        f"VALUES('{self.autor}', '{self.book_name}', '{self.bookmarks}')")
            self.con.commit()
        except Exception as e:
            print(e)
        self.close()

    def closes(self):
        self.close()


class DescriptionDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("description.ui", self)
        self.con = sqlite3.connect("system_files/ebook.db")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.append_elem)
        self.pushButton_4.clicked.connect(self.delete_elem)

        self.modified = {}
        self.titles = None

    def update_result(self):
        try:
            cur = self.con.cursor()
            if self.spinBox.text() != "0":
                result = cur.execute("SELECT * FROM description WHERE id=?",
                                     (item_id := self.spinBox.text(),)).fetchall()
                self.tableWidget.setRowCount(len(result))
                # Если запись не нашлась, то не будем ничего делать
                if not result:
                    self.statusBar().showMessage('Ничего не нашлось')
                    return
                else:
                    self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
                self.tableWidget.setColumnCount(len(result[0]))
                self.titles = [description[0] for description in cur.description]
                # Заполнили таблицу полученными элементами
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                self.modified = {}
            else:
                self.cur = self.con.cursor()
                tab1 = "SELECT * FROM description"
                try:
                    self.statusBar().showMessage('')
                    result = self.cur.execute(tab1).fetchall()
                    self.tableWidget.setRowCount(len(result))
                    self.tableWidget.setColumnCount(len(result[0]))
                    for i, elem in enumerate(result):
                        for j, val in enumerate(elem):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                except Exception as e:
                    print(e)
                self.modified = {}
        except Exception as e:
            print(e)

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM bookmarks WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()

    def append_elem(self):
        self.x = AppendDescription()
        self.x.show()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE description SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))

            self.con.commit()
            self.modified.clear()


class AppendDescription(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("append_description.ui", self)
        self.con = sqlite3.connect("system_files/ebook.db")
        self.ok_pressed.clicked.connect(self.remember_result)
        self.cancel_pressed.clicked.connect(self.closes)
        self.modified = {}
        self.titles = None

    def remember_result(self):
        try:
            self.autor = self.author.text()
            self.book_name = self.author.text()
            self.description = self.description.text()

            cur = self.con.cursor()
            cur.execute(f"INSERT INTO description(author, book_name, description)"
                        f"VALUES('{self.autor}', '{self.book_name}', '{self.description}')")
            self.con.commit()

        except Exception as e:
            print(e)
        self.close()

    def closes(self):
        self.close()


class Buttons(Main):
    def initUI(self):
        self.settings = QPushButton(self)
        self.settings.setIcon(QIcon('system_files/settings.png'))
        self.settings.setIconSize(QSize(20, 20))
        self.settings.move(468, 0)

        self.three_points = QPushButton(self)
        self.three_points.setIcon(QIcon('system_files/three_points.png'))
        self.three_points.setIconSize(QSize(20, 20))
        self.three_points.move(0, 0)

        self.title = QLabel(self)
        self.title.setFixedSize(460, 20)
        self.title.move(40, 0)
        self.title.setText("")

        self.text_lable = QTextEdit(self)
        self.text_lable.setFixedSize(500, 480)
        self.text_lable.move(0, 30)
        self.text_lable.setText("Выберите книгу из библиотеки")
        self.f = self.text_lable.font()
        self.f.setPointSize(14)  # sets the size to 27
        self.text_lable.setFont(self.f)
        self.text_lable.setReadOnly(True)

        self.show()

        # Создаем контекстное меню для 3точки
        context_menu_three_point = QMenu(self.three_points)
        action_book_description = QAction("описание книг", context_menu_three_point)
        action_table_of_contents = QAction("оглавление", context_menu_three_point)
        action_bookmarks = QAction("заметки", context_menu_three_point)
        action_read = QAction("аудиокнига", context_menu_three_point)
        action_library = QAction("библиотека", context_menu_three_point)
        action_file_selection = QAction("добавление файла", context_menu_three_point)
        action_leave_a_review = QAction("оставить отзыв", context_menu_three_point)

        action_book_description.triggered.connect(self.action_book_description)
        action_table_of_contents.triggered.connect(self.action_table_of_contents)
        action_bookmarks.triggered.connect(self.action_bookmarks)
        action_read.triggered.connect(self.action_read)
        action_library.triggered.connect(self.action_library)
        action_file_selection.triggered.connect(self.action_file_selection)
        action_leave_a_review.triggered.connect(self.action_leave_a_review)

        context_menu_three_point.addAction(action_book_description)
        context_menu_three_point.addAction(action_table_of_contents)
        context_menu_three_point.addAction(action_bookmarks)
        context_menu_three_point.addAction(action_read)
        context_menu_three_point.addAction(action_library)
        context_menu_three_point.addAction(action_file_selection)
        context_menu_three_point.addAction(action_leave_a_review)

        self.three_points.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.three_points.customContextMenuRequested.connect(
            lambda pos: context_menu_three_point.exec_(self.three_points.mapToGlobal(pos)))

        # создаем контекстное меню для настроек
        context_menu_settings = QMenu(self.settings)
        action_font_size = QAction("размер шрифта", context_menu_settings)
        action_help = QAction("помощь", context_menu_settings)
        action_color = QAction("цвет", context_menu_settings)
        action_font = QAction("редактировать отображение текста", context_menu_settings)
        action_about_the_program = QAction("о программе", context_menu_settings)

        action_font_size.triggered.connect(self.action_font_size)
        action_help.triggered.connect(self.action_help)
        action_font.triggered.connect(self.action_font)
        action_color.triggered.connect(self.action_color)
        action_about_the_program.triggered.connect(self.action_about_the_program)

        context_menu_settings.addAction(action_font_size)
        context_menu_settings.addAction(action_help)
        context_menu_settings.addAction(action_font)
        context_menu_settings.addAction(action_color)
        context_menu_settings.addAction(action_about_the_program)

        self.settings.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.settings.customContextMenuRequested.connect(
            lambda pos: context_menu_settings.exec_(self.settings.mapToGlobal(pos)))

    def action_book_description(self):
        try:
            self.ex = DescriptionDB()
            self.ex.show()
        except Exception as e:
            print(e)

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

    def action_leave_a_review(self):
        QMessageBox.about(self, "Отзыв", "Можете написать отзыв в телеграмм в личные сообщения. "
                                         "Мой профиль: https://t.me/nastya_ilyicheva")

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

    def closeEvent(self, evnt):
        answer = QMessageBox.question(
            self,
            'Confirmation',
            'Закрыть программу?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            evnt.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartDialogue()
    sys.exit(app.exec_())
