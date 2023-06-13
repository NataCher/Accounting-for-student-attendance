from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys


from dopclass import MainAppMenu, MainAppStudents
from dopclass import MainAppGroupe
from dopclass  import MainAppTeachers
from dopclass import MainAppSubjects
from dopclass import MainAppJournal
from dopclass import MainFormTimePair

ui, _ = loadUiType('shedule.ui')
journal_ui, _ = loadUiType('journal.ui')
timepair_ui, _ = loadUiType('timepair.ui')
timepair_ui, _ = loadUiType('timepair.ui')

class MainAppShedule(QMainWindow, ui):
    
    def __init__(self, parent=None):
        super(MainAppShedule, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db_connect()
        self.handles_btn()

        self.table_sh.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_sh.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/sh.ico'))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.table_sh.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # авт.растягивание колонок

        self.attendance_btn.clicked.connect(self.open_Journal_form)

        self.pair_btn.clicked.connect(self.open_TimePair_form)
        
        self.loaddata()  # Загрузка данных в таблицу

    def open_Journal_form(self):
        self.close()
        self.groupe_form = MainAppJournal()
        self.groupe_form.show()

    def open_TimePair_form(self):
        self.timepair_form = MainFormTimePair()
        self.timepair_form.show()   
        

    def db_connect(self):
        self.db = sqlite3.connect('db.sqlite')
        self.cur = self.db.cursor()
        if self.cur:
            self.messagebox("Сообщение проверки", "База данных db подключена")
        else:
            self.messagebox("Сообщение проверки", "База данных db не подключена")
            
    def loaddata(self):
        sql = "SELECT * FROM schedule LIMIT 250"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.table_sh.setRowCount(len(data))  # Устанавливаем количество строк таблицы равным количеству записей из базы данных

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.table_sh.setItem(row_index, column_index, item)

                self.table_sh.resizeColumnsToContents()  # Растягиваем столбцы таблицы для лучшего отображения данных

    def Add_Shedule(self):
        ID = self.lineEdit_2_sh.text()
        # Проверяем наличие дубликата
        if self.check_duplicate(ID):
            self.messagebox("Сообщение", "Запись с таким ID уже существует")
            return
        # Продолжаем добавление записи
        weekday = self.lineEdit_3_sh_3.text()
        date = self.lineEdit_4_sh.text()
        group_id = self.lineEdit_sh.text()
        pair_id = self.lineEdit_6__sh.text()
        subject_id = self.lineEdit_3_sh.text()
        type_ = self.lineEdit_3_sh_2.text()
        teacher_id = self.lineEdit_7_sh.text()
        cabinet = self.lineEdit_8__sh.text()

        if ID:
            self.cur.execute('''
                INSERT INTO schedule (ID, weekday, date, group_id, pair_id, subject_id, type_, teacher_id, cabinet)
                VALUES(?,?,?,?,?,?,?,?,?)''', (ID, weekday, date, group_id, pair_id, subject_id, type_, teacher_id, cabinet))
            self.db.commit()
            self.messagebox("Сообщение", "Запись группы была успешно добавлена")
            self.loaddata()  # Обновление таблицы после добавления записи
        else:
            self.messagebox("Сообщение", "Введите данные для записи в базу данных")


    def Update_Shedule(self):
        ID = self.lineEdit_2_sh.text()
        if ID:
            weekday = self.lineEdit_3_sh_3.text()
            date = self.lineEdit_4_sh.text()
            group_id = self.lineEdit_sh.text()
            pair_id = self.lineEdit_6__sh.text()
            subject_id = self.lineEdit_3_sh.text()
            type_ = self.lineEdit_3_sh_2.text()
            teacher_id = self.lineEdit_7_sh.text()
            cabinet = self.lineEdit_8__sh.text()

            self.cur.execute('''
                UPDATE schedule SET weekday=?, date=?, group_id=?, pair_id=?, subject_id=?, type_=?, teacher_id=?, cabinet=? WHERE ID=?
                ''', (weekday, date, group_id, pair_id, subject_id, type_, teacher_id, cabinet, ID))
            self.db.commit()
            self.Clear()
            self.messagebox("Сообщение", "Запись обновлена")
            self.loaddata()  # Обновление таблицы после обновления записи
        else:
            self.messagebox("Сообщение", "Запись не обновлена")

    def Delete_Shedule(self):
        ID = self.lineEdit_2_sh.text()
        if ID:
            self.cur.execute('''DELETE FROM schedule WHERE ID=?''', (ID,))
            self.db.commit()
            self.Clear()
            self.messagebox("Сообщение", "Запись удалена")
            self.loaddata()  # Обновление таблицы после удаления записи
        else:
            self.messagebox("Сообщение", "Запись не удалена")

    def Clear(self):
        self.lineEdit_2_sh.setText("")
        self.lineEdit_3_sh_3.setText("")
        self.lineEdit_4_sh.setText("")
        self.lineEdit_sh.setText("")
        self.lineEdit_6__sh.setText("")
        self.lineEdit_3_sh.setText("")
        self.lineEdit_3_sh_2.setText("")
        self.lineEdit_7_sh.setText("")
        self.lineEdit_8__sh.setText("")
        self.lineEdit_seatch_sh.setText("")

    def clear_table(self):
      
        self.table_sh.setRowCount(0)
        self.table_sh.clearContents()

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/message.png'))
        mess.exec_()

    def handles_btn(self):
        self.btn_Insert__sh.clicked.connect(self.Add_Shedule)
        self.Search_btn_sh.clicked.connect(self.Search_Shedule)
        self.deletezapic__sh.clicked.connect(self.Delete_Shedule)
        self.clears_sh.clicked.connect(self.Clear)
        self.cleant__sh.clicked.connect(self.clear_table)
        self.vuvod__sh.clicked.connect(self.loaddata)  # Связь с кнопкой "Вывод данных"

        self.shedule_btn.clicked.connect(self.open_main_menu)
            
    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()      
        
    def Search_Shedule(self):
        ID = self.lineEdit_seatch_sh.text()
        sql = '''SELECT * FROM schedule WHERE ID=? '''
        self.cur.execute(sql, [(ID)])
        data = self.cur.fetchone()
        if ID == "":
            self.messagebox("Сообщение", "Введите ID для поиска записи")
        elif data:
            self.lineEdit_2_sh.setText(str(data[0]))
            self.lineEdit_3_sh_3.setText(str(data[1]))
            self.lineEdit_4_sh.setText(str(data[2]))
            self.lineEdit_sh.setText(str(data[3]))
            self.lineEdit_6__sh.setText(str(data[4]))
            self.lineEdit_3_sh.setText(str(data[5]))
            self.lineEdit_3_sh_2.setText(str(data[6]))
            self.lineEdit_7_sh.setText(str(data[7]))
            self.lineEdit_8__sh.setText(str(data[8]))
        else:
            self.messagebox("Сообщение", "Запись не найдена")

    def check_duplicate(self, ID):
        sql = "SELECT * FROM schedule WHERE ID=?"
        self.cur.execute(sql, (ID,))
        data = self.cur.fetchone()
        if data:
            return True  # Запись с заданным ID уже существует
        else:
            return False  # Запись с заданным ID не существует

def main():
    app = QApplication(sys.argv)
    window = MainAppShedule()
    window.setFixedSize(1891, 973)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
