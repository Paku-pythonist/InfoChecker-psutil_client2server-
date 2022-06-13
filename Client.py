from PyQt5 import QtCore, QtGui, QtWidgets
from visual_client import *
import socket
from time import sleep
import time
import psutil
import datetime
import struct
import json
import sys
import os
import platform


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------CLIENT----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Некоторые переменные
        self.worker = False

        # Style clicked menu button
        for w in self.ui.frame_2.findChildren(QtWidgets.QPushButton):
            w.clicked.connect(self.applyButtonStyle)  # Add click event listener

        # Функционал кнопок
        self.ui.pushButton_connect.clicked.connect(lambda: self.applyButtonStyle)

        self.show()

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------Set Connection with Client-----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def work(self):
        HOST = str(self.ui.lineEdit_HOST.text())
        PORT = int(self.ui.lineEdit_PORT.text())

        try:
            # нужно создать сокет, подключиться к серверу послать ему данные, принять данные и закрыть соединение
            client_socket = socket.socket()
            client_socket.connect((HOST, PORT))  # подключаемся к серверу

            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if data:
                    message = json.loads(data)
                    print("   Сервер:", message["start"])
                    sleep(0.1)

                    # Формирование Данных для Откправки, а также Построчная Отправка
                    for x in psutil.pids():
                        try:
                            # Данные для ТЗ
                            process = psutil.Process(x)
                            count = str(len(psutil.pids()))
                            pid = str(process.pid)
                            name = process.name()
                            status = process.status()
                            my_time = str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S'))
                            rss = round(process.memory_info().rss / (1024 * 1024), 2)

                            # Данные для идентификации пользователя и разграничения БД
                            node = platform.node()  # Имя Компьютера
                            login = os.getlogin()  # Имя Пользователя
                            page_name = time.ctime()[8:11] + time.ctime()[4:8] + time.ctime()[-4:] + time.ctime()[10:19]


                            message = bytes(json.dumps({"count": count, "pid": pid, "name": name, "status": status, "my_time": my_time, "rss": rss,
                                                        "node": node, "login": login,  "page_name": page_name}), encoding="utf-8")

                            client_socket.sendall(message)   # сериализация
                            # print(message)
                            sleep(0.001)

                        except Exception as e:
                            # print(e, '\n')
                            pass

                    # далее будем получать данныеи небольшими порциями
                    while True:
                        data = client_socket.recv(1024).decode("utf-8")
                        if data:
                            message = json.loads(data)
                            print(message["finish"])
                            sleep(0.1)
                            # self.work()

                        else:
                            break


                    # message = bytes(json.dumps({"finish": "   finish"}), encoding="utf-8")
                    # client_socket.sendall(message)
                    # print(message)
                    # # break
                else:
                    print(0)
                    break





            client_socket.close()
            self.work()

        except Exception as e:
            self.sender().setStyleSheet("border-bottom: none;")
            print("Ошибка! ", e)
            self.applyButtonStyle()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------Side Menu buttons styling function--------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def applyButtonStyle(self):
        if self.worker == True:
            print("Клиент: ВЫКЛ \n")
            self.sender().setStyleSheet("border-bottom: none; background-color: rgb(141, 141, 141);")
            self.worker = False
        else:
            print("\nКлиент: ВКЛ")
            self.sender().setStyleSheet("border-bottom: 2px solid; background-color: rgb(141, 141, 141);")
            self.worker = True
            self.work()
        return
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------Запуск визуалки-------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())








