from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

from dopclass import MainAppMenu

subjects_ui, _= loadUiType('subjects.ui')

class MainAppSubjects(QMainWindow, subjects_ui):
    def __init__(self, parent=None):
        super(MainAppSubjects, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db_connect()
        self.handles_btn()

        self.table_sub.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_sub.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/sub.ico'))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.table_sub.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # авт.растягивание колонок

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
        self.Insert_dis.clicked.connect(self.Add_Subjects)
        self.Search_btn_sub.clicked.connect(self.Search_Subjects)
        self.deletezapic_sub.clicked.connect(self.Delete_Subjects)
        self.clears_sub.clicked.connect(self.Clear)
        self.update_sub.clicked.connect(self.Update_Subjects)
        self.vuvod_sub.clicked.connect(self.loaddata)
        self.cleant_sub.clicked.connect(self.clear_table)

        self.subject_btn.clicked.connect(self.open_main_menu)

    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()

    def Add_Subjects(self):
        ID = self.lineEdit2.text()
        indexx = self.lineEdit3.text()
        name = self.lineEdit4.text()
        if ID and indexx and name != "":
            # Проверка на повторение записей
            self.cur.execute("SELECT * FROM subjects WHERE ID=?", (ID,))
            existing_record = self.cur.fetchone()
            if existing_record:
                self.messagebox("Сообщение", "Запись с таким ID уже существует")
            else:
                self.cur.execute('''
                    INSERT INTO subjects (ID, indexx, name)
                    VALUES(?, ?, ?)''', (ID, indexx, name))
                self.db.commit()
                self.messagebox("Сообщение", "Запись успешно добавлена")
                self.loaddata()  # Update the table
        else:
            self.messagebox("Сообщение", "Введите данные для записи в базу данных")

    def Search_Subjects(self):
        ID = self.lineEdit_seatch_sub.text()
        sql = '''SELECT * FROM subjects WHERE ID=? '''
        self.cur.execute(sql, [(ID)])
        data = self.cur.fetchone()
        if ID == "":
            self.messagebox("Сообщение", "Введите ID для поиска записи")
        elif data:
            self.lineEdit2.setText(str(data[0]))
            self.lineEdit3.setText(str(data[1]))
            self.lineEdit4.setText(str(data[2]))
        else:
            self.messagebox("Сообщение", "Нет записи в БД")

    def Delete_Subjects(self):
        ID = self.lineEdit2.text()
        if ID:
            sql = '''DELETE FROM subjects WHERE ID=?'''
            self.cur.execute(sql, [(ID)])
            self.db.commit()
            self.Clear()
            self.loaddata()  # Update the table
        else:
            self.messagebox("Сообщение", "Введите ID для удаления записи")

    def Clear(self):
        self.lineEdit2.setText("")
        self.lineEdit3.setText("")
        self.lineEdit4.setText("")
        self.lineEdit_seatch_sub.setText("")

    def clear_table(self):
        self.table_sub.setRowCount(0)

    def Update_Subjects(self):
        ID = self.lineEdit2.text()
        if ID:
            self.cur.execute("SELECT * FROM subjects WHERE ID=?", (ID,))
            existing_record = self.cur.fetchone()
            if existing_record:
                indexx = self.lineEdit3.text()
                name = self.lineEdit4.text()
                self.cur.execute('''
                    UPDATE subjects SET ID=?, indexx=?, name=? WHERE ID=?
                ''', (ID, indexx, name, ID))
                self.db.commit()
                self.Clear()
                self.messagebox("Сообщение", "Запись обновлена")
                self.loaddata()  # Update the table
            else:
                self.messagebox("Сообщение", "Записи с указанным ID не существует")
        else:
            self.messagebox("Сообщение", "Запись не обновлена")

    def loaddata(self):
        self.table_sub.setRowCount(0)
        sql = '''SELECT * FROM subjects LIMIT 50'''
        tablerow = 0
        for row in self.cur.execute(sql):
            self.table_sub.insertRow(tablerow)
            self.table_sub.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.table_sub.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.table_sub.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1
        self.table_sub.resizeColumnsToContents()

def main():
    app = QApplication(sys.argv)
    window = MainAppSubjects()
    window.setFixedSize(1530, 792) 
    window.show()
    app.exec_()


    
    
if __name__ == '__main__':
    main()

