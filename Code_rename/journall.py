from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

from dopclass import MainAppMenu, MainAppShedule, MainAppStudents
from dopclass import MainAppGroupe
from dopclass  import MainAppTeachers
from dopclass import MainAppSubjects
from dopclass import MainAppJournal

ui, _ = loadUiType('journal.ui')
shedule_ui, _ = loadUiType('shedule.ui')

class MainAppJournal(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainAppJournal, self).__init__(parent)
        self.setupUi(self)
        self.db_connect()
        self.handles_btn()

        self.loaddata()

        self.table__att.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table__att.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/bl.jpg'))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        self.shedule_btn.clicked.connect(self.open_shedule_form)

    def open_shedule_form(self):
        self.close()
        self.shedule_form = MainAppShedule()
        self.shedule_form.show()

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
        self.btn_Insert__att.clicked.connect(self.Add_Journal)
        self.Search_btn_att.clicked.connect(self.Search_Journal)
        self.deletezapic__att.clicked.connect(self.Delete_Journal)
        self.clears__att.clicked.connect(self.Clear)
        self.update___att.clicked.connect(self.Update_Journal)
        self.vuvod___att.clicked.connect(self.loaddata)
        self.cleant_v_att.clicked.connect(self.clear_table)

        self.back_to_menu.clicked.connect(self.open_main_menu)

    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()

    def Add_Journal(self):
        ID = self.lineEdit_2_att.text()
        if not ID:
            self.messagebox("Сообщение", "Введите данные для записи в базу данных")
            return

        # Проверка повторений записи
        sql_check = "SELECT * FROM attendance WHERE ID = ?"
        self.cur.execute(sql_check, [(ID)])
        data = self.cur.fetchone()
        if data:
            self.messagebox("Сообщение", "Запись с таким ID уже существует")
            return

        student_id = self.lineEdit_7_att.text()
        shedule_id = self.lineEdit_4_att.text()
        pair1 = self.lineEdit_att.text()
        pair2 = self.lineEdit_6___att.text()
        pair3 = self.lineEdit_3_att.text()
        pair4 = self.lineEdit_3__att.text()
        mark = self.lineEdit_3__att_2.text()
        comment = self.lineEdit_8__att.text()

        self.cur.execute('''
            INSERT INTO attendance (ID, student_id, shedule_id, pair1, pair2, pair3, pair4, mark, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (ID, student_id, shedule_id, pair1, pair2, pair3, pair4, mark, comment))
        self.db.commit()
        self.messagebox("Сообщение", "Запись журнала была успешно добавлена")
        self.Clear()
        self.loaddata()

    def Search_Journal(self):
        ID = self.lineEdit_seatch__att.text()
        sql = '''SELECT * FROM attendance WHERE ID = ?'''
        self.cur.execute(sql, [(ID)])
        data = self.cur.fetchone()
        if ID == "":
            self.messagebox("Сообщение", "Введите ID для поиска записи")
        elif data:
            self.lineEdit_2_att.setText(str(data[0]))
            self.lineEdit_7_att.setText(str(data[1]))
            self.lineEdit_4_att.setText(str(data[2]))
            self.lineEdit_att.setText(str(data[3]))
            self.lineEdit_6___att.setText(str(data[4]))
            self.lineEdit_3_att.setText(str(data[5]))
            self.lineEdit_3__att.setText(str(data[6]))
            self.lineEdit_3__att_2.setText(str(data[7]))
            self.lineEdit_8__att.setText(str(data[8]))
        else:
            self.messagebox("Сообщение", "Нет записи в БД")

    def Delete_Journal(self):
        ID = self.lineEdit_2_att.text()
        sql = '''DELETE FROM attendance WHERE ID = ?'''
        self.cur.execute(sql, [(ID)])
        self.db.commit()
        self.Clear()
        self.loaddata()

    def Clear(self):
        self.lineEdit_2_att.setText("")
        self.lineEdit_7_att.setText("")
        self.lineEdit_4_att.setText("")
        self.lineEdit_att.setText("")
        self.lineEdit_6___att.setText("")
        self.lineEdit_3_att.setText("")
        self.lineEdit_3__att.setText("")
        self.lineEdit_3__att_2.setText("")
        self.lineEdit_8__att.setText("")
        self.lineEdit_seatch__att.setText("")

    def clear_table(self):
        self.table__att.clearContents()
        self.table__att.setRowCount(0)

    def Update_Journal(self):
        ID = self.lineEdit_2_att.text()
        if not ID:
            self.messagebox("Сообщение", "Запись не обновлена")
            return

        student_id = self.lineEdit_7_att.text()
        shedule_id = self.lineEdit_4_att.text()
        pair1 = self.lineEdit_att.text()
        pair2 = self.lineEdit_6___att.text()
        pair3 = self.lineEdit_3_att.text()
        pair4 = self.lineEdit_3__att.text()
        mark = self.lineEdit_3__att_2.text()
        comment = self.lineEdit_8__att.text()

        self.cur.execute('''
            UPDATE attendance SET ID = ?, student_id = ?, shedule_id = ?, pair1 = ?, pair2 = ?, pair3 = ?, pair4 = ?, mark = ?, comment = ?
            WHERE ID = ?''',
            (ID, student_id, shedule_id, pair1, pair2, pair3, pair4, mark, comment, ID))
        self.db.commit()
        self.Clear()
        self.messagebox("Сообщение", "Запись обновлена")
        self.loaddata()

    def loaddata(self):
        self.table__att.clearContents()
        connection = sqlite3.connect('db.sqlite')
        cur = connection.cursor()
        sql = '''SELECT * FROM attendance LIMIT 500'''
        cur.execute(sql)
        data = cur.fetchall()
        self.table__att.setRowCount(len(data))  # Устанавливаем количество строк таблицы равным количеству записей из базы данных

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.table__att.setItem(row_index, column_index, item)

        self.table__att.resizeColumnsToContents()  # Растягиваем столбцы таблицы для лучшего отображения данных


def main():
    app = QApplication(sys.argv)
    window = MainAppJournal()
    window.setFixedSize(1707, 880)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
