import sys
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class BookmarksDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("system_files/bookmarks.ui", self)
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
        uic.loadUi("system_files/append_bookmarks.ui", self)
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