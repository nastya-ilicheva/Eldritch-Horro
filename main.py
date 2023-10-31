import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QPushButton, QTextEdit


class Example(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()
        age, ok_pressed = QInputDialog.getInt(
            self, "Введите возраст", "Сколько тебе лет?",
            1, 1, 8, 1)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Eldrich Horror')



        # self.button_1 = QPushButton(self)
        # self.button_1.move(20, 40)
    #     self.button_1.setText("Кнопка")
    #     self.button_1.clicked.connect(self.run)
    #
    # def run(self):
    #     name, ok_pressed = QInputDialog.getText(self, "Введите имя",
    #                                             "Как тебя зовут?")
    #     if ok_pressed:
    #         self.button_1.setText(name)


if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = Example()
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())