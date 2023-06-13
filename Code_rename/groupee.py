from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

menu_ui, _ = loadUiType('menu.ui')
groupe_ui, _ = loadUiType('groupe.ui')

from dopclass import MainAppMenu

class MainAppGroupe(QMainWindow, groupe_ui):
    def __init__(self, parent=None):
        super(MainAppGroupe, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/people.png'))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.handles_btn()
        self.db_connect()

        self.load_data()

    def db_connect(self):
        self.db = sqlite3.connect('db.sqlite')
        self.cur = self.db.cursor()
        if self.cur:
            self.message_box("Сообщение проверки", "База данных db подключена")
        else:
            self.message_box("Сообщение проверки", "База данных db не подключена")

    def message_box(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setWindowIcon(QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/message.png'))
        mess.exec_()

    def handles_btn(self):
        self.btn_Insert.clicked.connect(self.add_group)
        self.Search_btn_sub.clicked.connect(self.search_group)
        self.deletezapic_2.clicked.connect(self.delete_group)
        self.clears.clicked.connect(self.clear)
        self.update_gr.clicked.connect(self.update_group)
        self.vuvod.clicked.connect(self.load_data)
        self.cleant.clicked.connect(self.clear_table)
        self.back_to_menu.clicked.connect(self.open_main_menu)

    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()

    def add_group(self):
        ID = self.lineEdit_2.text()
        number = self.lineEdit_3.text()
        speciality = self.lineEdit_4.text()
        if ID and number and speciality != "":
            self.cur.execute('SELECT * FROM groups WHERE ID=?', (ID,))
            existing_record = self.cur.fetchone()
            if existing_record:
                self.message_box("Сообщение", "Запись с таким ID уже существует")
            else:
                self.cur.execute('''
                        INSERT INTO groups (ID, number, speciality)
                        VALUES(?,?,?)''', (ID, number, speciality))
                self.db.commit()
                self.message_box("Сообщение", "Запись группы была успешно добавлена")
                self.load_data() 
        else:
            self.message_box("Сообщение", "Введите данные для записи в базу данных")

    def search_group(self):
        ID = self.lineEdit_seatch.text()
        sql = '''SELECT * FROM groups WHERE ID=?'''
        self.cur.execute(sql, [(ID)])
        data = self.cur.fetchone()
        if ID == "":
            self.message_box("Сообщение", "Введите ID для поиска записи")
        elif data:
            self.lineEdit_2.setText(str(data[0]))
            self.lineEdit_3.setText(str(data[1]))
            self.lineEdit_4.setText(str(data[2]))
        else:
            self.message_box("Сообщение", "Нет записи в БД")

    def delete_group(self):
        ID = self.lineEdit_2.text()
        data = self.cur.fetchone()
        sql = '''DELETE FROM groups WHERE ID=?'''
        self.cur.execute(sql, [(ID)])
        self.db.commit()
        self.clear()
        self.load_data() 

    def clear(self):
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_seatch.setText("")

    def clear_table(self):
        self.table.setRowCount(0)

    def update_group(self):
        ID = self.lineEdit_2.text()
        if ID:
            ID = self.lineEdit_2.text()
            number = self.lineEdit_3.text()
            speciality = self.lineEdit_4.text()
            self.cur.execute('''
                                UPDATE groups SET ID=?, number=?, speciality=? WHERE ID=?
                                ''', (ID, number, speciality, ID))
            self.db.commit()
            self.clear()
            self.message_box("Сообщение", "Запись обновлена")
            self.load_data() 
        else:
            self.message_box("Сообщение", "Запись не обновлена")

    def load_data(self):
        connection = sqlite3.connect('db.sqlite')
        cur = connection.cursor()
        self.cur.execute('SELECT * FROM groups LIMIT 300')
        rows = self.cur.fetchall()
        self.table.setRowCount(len(rows))
        for row_num, row_data in enumerate(rows):
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))
        self.table.resizeColumnsToContents()        


def main():
    app = QApplication(sys.argv)
    window = MainAppGroupe()
    window.setFixedSize(1631, 777)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
