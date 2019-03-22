import sys
from figures import *
from algos import *
import gui
from PyQt5 import QtWidgets


class MainApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
