from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

from dopclass import MainAppMenu

teachers_ui, _ = loadUiType('teachers.ui')

class MainAppTeachers(QMainWindow, teachers_ui):
    def __init__(self, parent=None):
        super(MainAppTeachers, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db_connect()
        self.handles_btn()

        self.table_tea.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_tea.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/training.png'))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.table_tea.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # авт.растягивание колонок

        self.loaddata()

    def db_connect(self):
        self.db = sqlite3.connect('db.sqlite')
        self.cur = self.db.cursor()
        if self.cur:
            self.messagebox("Сообщение проверки", "База данных db подключена")
        else:
            self.messagebox("Сообщение проверки", "База данных db не подключена")

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/message.png'))
        mess.exec_()

    def handles_btn(self):
        self.btn_Insert_tea.clicked.connect(self.Add_Teachers)
        self.Search_btn_tea.clicked.connect(self.Search_Teachers)
        self.deletezapic_tea.clicked.connect(self.Delete_Teachers)
        self.clears_tea.clicked.connect(self.Clear)
        self.update_tea.clicked.connect(self.Update_Teachers)
        self.vuvod_tea.clicked.connect(self.loaddata)
        self.cleant_tea.clicked.connect(self.clear_table)

        self.teachers_btn.clicked.connect(self.open_main_menu)

    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()

    def Add_Teachers(self):
        ID = self.lineEdit_2_tea.text()
        surname = self.lineEdit_3_tea.text()
        name = self.lineEdit_4_tea.text()
        patronymic = self.lineEdit_tea.text()
        mail = self.lineEdit_8_tea.text()
        phone = self.lineEdit_6_tea.text()
        subject_id = self.lineEdit_5_tea.text()

        if ID and surname and name and patronymic and mail and phone and subject_id != "":
            self.cur.execute("SELECT * FROM teachers WHERE ID=?", (ID,))
            existing_data = self.cur.fetchone()
            if existing_data:
                self.messagebox("Ошибка", "Запись с таким ID уже существует")
                return

            self.cur.execute(
                '''INSERT INTO teachers (ID, surname, name, patronymic, mail, phone, subject_id)
                VALUES(?,?,?,?,?,?,?)''', (ID, surname, name, patronymic, mail, phone, subject_id))
            self.db.commit()
            self.messagebox("Сообщение", "Запись успешно добавлена")
            self.loaddata()  # Update the table
        else:
            self.messagebox("Сообщение", "Введите данные для записи в базу данных")

    def Search_Teachers(self):
        ID = self.lineEdit_seatch_tea.text()
        sql = '''SELECT * FROM teachers WHERE ID=? '''
        self.cur.execute(sql, [(ID)])
        data = self.cur.fetchone()
        if ID == "":
            self.messagebox("Сообщение", "Введите ID для поиска записи")
        elif data:
            self.lineEdit_2_tea.setText(str(data[0]))
            self.lineEdit_3_tea.setText(str(data[1]))
            self.lineEdit_4_tea.setText(str(data[2]))
            self.lineEdit_tea.setText(str(data[3]))
            self.lineEdit_8_tea.setText(str(data[4]))
            self.lineEdit_6_tea.setText(str(data[5]))
            self.lineEdit_5_tea.setText(str(data[6]))
        else:
            self.messagebox("Сообщение", "Нет записи в БД")

    def Delete_Teachers(self):
        ID = self.lineEdit_2_tea.text()
        data = self.cur.fetchone()
        sql = '''DELETE FROM teachers WHERE ID=?'''
        self.cur.execute(sql, [(ID)])

        self.db.commit()
        self.Clear()
        self.loaddata()

    def Clear(self):
        self.lineEdit_2_tea.setText("")
        self.lineEdit_3_tea.setText("")
        self.lineEdit_4_tea.setText("")
        self.lineEdit_tea.setText("")
        self.lineEdit_8_tea.setText("")
        self.lineEdit_6_tea.setText("")
        self.lineEdit_5_tea.setText("")

        self.lineEdit_seatch_tea.setText("")

    def clear_table(self):
        self.table_tea.setRowCount(0)

    def Update_Teachers(self):
        ID = self.lineEdit_2_tea.text()
        if ID:
            ID = self.lineEdit_2_tea.text()
            surname = self.lineEdit_3_tea.text()
            name = self.lineEdit_4_tea.text()
            patronymic = self.lineEdit_tea.text()
            mail = self.lineEdit_8_tea.text()
            phone = self.lineEdit_6_tea.text()
            subject_id = self.lineEdit_5_tea.text()

            self.cur.execute('''
                UPDATE teachers SET ID=?, surname=?, name=?, patronymic=?, mail=?, phone=?, subject_id=?  WHERE ID=?
                ''', (ID, surname, name, patronymic, mail, phone, subject_id, ID))
            self.db.commit()
            self.Clear()
            self.messagebox("Сообщение", "Запись обновлена")
            self.loaddata()  # Update the table
        else:
            self.messagebox("Сообщение", "Запись не обновлена")

    def loaddata(self):
        self.table_tea.clearContents()
        connection = sqlite3.connect('db.sqlite')
        cur = connection.cursor()
        sql = '''SELECT * FROM teachers LIMIT 100'''
        cur.execute(sql)
        data = cur.fetchall()
        row_count = len(data)
        self.table_tea.setRowCount(row_count)
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.table_tea.setItem(row_num, col_num, item)
                
        self.table_tea.resizeColumnsToContents()

def main():
    app = QApplication(sys.argv)
    window = MainAppTeachers()
    window.setFixedSize(1572, 842)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
