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
        self.library = []

    def initUI(self):
        self.setWindowTitle('eBook')
        e = Buttons()


class StartDialogue(QDialog):
    def __init__(self):
        super(StartDialogue, self).__init__()

        self.answer = QMessageBox.question(
            self,
            'Confirmation',
            'Do you want to start?',
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


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.con = sqlite3.connect("ebook.db")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)

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

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE description SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))

            self.con.commit()
            self.modified.clear()


class Buttons(Main):
    def initUI(self):
        self.settings = QPushButton(self)
        self.settings.setIcon(QIcon('settings.png'))
        self.settings.setIconSize(QSize(20, 20))
        self.settings.move(470, 0)

        self.three_points = QPushButton(self)
        self.three_points.setIcon(QIcon('three_points.png'))
        self.three_points.setIconSize(QSize(20, 20))
        self.three_points.move(0, 0)

        self.title = QLabel(self)
        self.title.setFixedSize(150, 20)
        self.title.move(200, 0)
        self.title.setText("")

        self.text_lable = QTextEdit(self)
        self.text_lable.setFixedSize(500, 480)
        self.text_lable.move(0, 30)
        self.text_lable.setText("Select a book from the library")
        self.f = self.text_lable.font()
        self.f.setPointSize(14)  # sets the size to 27
        self.text_lable.setFont(self.f)
        self.text_lable.setReadOnly(True)

        self.show()

        # Создаем контекстное меню для 3точки
        context_menu_three_point = QMenu(self.three_points)
        action_book_description = QAction("book description", context_menu_three_point)
        action_table_of_contents = QAction("table of contents", context_menu_three_point)
        action_bookmarks = QAction("bookmarks", context_menu_three_point)
        action_read = QAction("read", context_menu_three_point)
        action_library = QAction("library", context_menu_three_point)
        action_file_selection = QAction("file selection", context_menu_three_point)
        action_leave_a_review = QAction("leve a review", context_menu_three_point)

        # Присоединяем действия к соответствующим функциям
        action_book_description.triggered.connect(self.action_book_description)
        action_table_of_contents.triggered.connect(self.action_table_of_contents)
        action_bookmarks.triggered.connect(self.action_bookmarks)
        action_read.triggered.connect(self.action_read)
        action_library.triggered.connect(self.action_library)
        action_file_selection.triggered.connect(self.action_file_selection)
        action_leave_a_review.triggered.connect(self.action_leave_a_review)

        # Добавляем пункты меню к контекстному меню
        context_menu_three_point.addAction(action_book_description)
        context_menu_three_point.addAction(action_table_of_contents)
        context_menu_three_point.addAction(action_bookmarks)
        context_menu_three_point.addAction(action_read)
        context_menu_three_point.addAction(action_library)
        context_menu_three_point.addAction(action_file_selection)
        context_menu_three_point.addAction(action_leave_a_review)

        # Прикрепляем контекстное меню к кнопке
        self.three_points.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.three_points.customContextMenuRequested.connect(
            lambda pos: context_menu_three_point.exec_(self.three_points.mapToGlobal(pos)))

        # создаем контекстное меню для настроек
        context_menu_settings = QMenu(self.settings)
        action_font_size = QAction("font size", context_menu_settings)
        action_help = QAction("help", context_menu_settings)
        action_extra_settings = QAction("extra settings", context_menu_settings)
        action_pictures = QAction("pictures", context_menu_settings)
        action_about_the_program = QAction("about the program", context_menu_settings)

        action_font_size.triggered.connect(self.action_font_size)
        action_help.triggered.connect(self.action_help)
        action_extra_settings.triggered.connect(self.action_extra_settings)
        action_pictures.triggered.connect(self.action_pictures)
        action_about_the_program.triggered.connect(self.action_about_the_program)

        context_menu_settings.addAction(action_font_size)
        context_menu_settings.addAction(action_help)
        context_menu_settings.addAction(action_extra_settings)
        context_menu_settings.addAction(action_pictures)
        context_menu_settings.addAction(action_about_the_program)

        self.settings.setContextMenuPolicy(3)  # 3 - Qt.CustomContextMenu
        self.settings.customContextMenuRequested.connect(
            lambda pos: context_menu_settings.exec_(self.settings.mapToGlobal(pos)))

    def action_book_description(self):
        pass

    def action_table_of_contents(self):
        pass

    def action_bookmarks(self):
        try:
            self.ex = MyWidget()
            self.ex.show()
        except Exception as e:
            print(e)

    def action_tp_to_the_page(self):
        pass

    def action_read(self):
        pass

    def action_library(self):
        book_name, ok_pressed = QInputDialog.getItem(
            self, "file", "choose book",
            tuple(self.library), 1, False)
        self.f.setPointSize(10)  # sets the size to 27
        self.text_lable.setFont(self.f)

        if ok_pressed:
            try:
                self.text_lable.clear()
                with io.open(book_name, encoding='utf-8') as file:
                    for i in file:
                        self.text_lable.append(i)
            except Exception as e:
                print(e)

    def action_file_selection(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'open file', '',
            'book (*.txt)')[0]
        self.library.append(self.fname)
        QMessageBox.about(self, "Title", "the file has been added to the library")

    def action_leave_a_review(self):
        pass

    def action_font_size(self):
        pass

    def action_help(self):
        pass

    def action_extra_settings(self):
        pass

    def action_pictures(self):
        pass

    def action_about_the_program(self):
        pass

    def closeEvent(self, evnt):
        answer = QMessageBox.question(
            self,
            'Confirmation',
            'Do you want to quit?',
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
