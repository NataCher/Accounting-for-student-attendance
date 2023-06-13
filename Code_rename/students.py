from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

from dopclass import MainAppMenu

students_ui, _= loadUiType('students.ui')
class MainAppStudents(QMainWindow,students_ui):
    
    def __init__(self, parent=None):
        super(MainAppStudents, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db_connect()   
        self.handles_btn()

        self.table_st.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_st.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/graduated.png'))
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        self.table_st.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #авт.растягивание колонок

        self.loaddata()
        
    def db_connect(self):
        self.db = sqlite3.connect('db.sqlite')
        self.cur = self.db.cursor()
        if(self.cur):
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
            self.btn_Insert_st.clicked.connect(self.Add_Students)
            self.Search_btn_st.clicked.connect(self.Search_Students)
            self.deletezapic_st.clicked.connect(self.Delete_Students)
            self.clears_st.clicked.connect(self.Clear)
            self.update_st.clicked.connect(self.Update_Students)
            self.vuvod_st.clicked.connect(self.loaddata)
            self.cleant_st.clicked.connect(self.clear_table)

            self.student_btn.clicked.connect(self.open_main_menu)
            
    def open_main_menu(self):
        self.close()
        self.main_menu = MainAppMenu()
        self.main_menu.show()
                   
    def Add_Students(self):
        ID = self.lineEdit_2_st.text()
        surname = self.lineEdit_3_st.text()
        name = self.lineEdit_4_st.text()
        patronymic = self.lineEdit_st.text()
        gender = self.lineEdit_6_st_2.text() 
        number = self.lineEdit_6_st.text()
        id_groupe = self.lineEdit_5_st.text()
        mail = self.lineEdit_7_st.text()
        phone = self.lineEdit_8_st.text()

        if ID and surname and name and patronymic and gender and number and id_groupe and mail and phone != "":
            self.cur.execute('SELECT * FROM students WHERE ID=?', (ID,))
            data = self.cur.fetchone()
            if data:
                self.messagebox("Ошибка", "Запись с таким ID уже существует")
            else:
                self.cur.execute('''
                    INSERT INTO students (ID, surname, name, patronymic, gender, number, id_groupe, mail, phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ID, surname, name, patronymic, gender, number, id_groupe, mail, phone))
                self.db.commit()
                self.messagebox("Сообщение", "Запись группы была успешно добавлена")
                self.loaddata()
        else: 
            self.messagebox("Сообщение", "Введите данные для записи в базу данных")

  
    def Search_Students(self):
        ID = self.lineEdit_seatch_st.text()
        sql =('''SELECT * FROM students WHERE ID=? ''')
        self.cur.execute(sql,[(ID)])
        data = self.cur.fetchone()
        if ID=="":
             self.messagebox("Сообщение", "Введите ID для поиска записи")
        elif (data):
                self.lineEdit_2_st.setText(str(data[0]))
                self.lineEdit_3_st.setText(str(data[1]))
                self.lineEdit_4_st.setText(str(data[2]))
                self.lineEdit_st.setText(str(data[3]))
                self.lineEdit_6_st_2.setText(str(data[4]))
                self.lineEdit_6_st.setText(str(data[5]))
                self.lineEdit_5_st.setText(str(data[6]))
                self.lineEdit_7_st.setText(str(data[7]))
                self.lineEdit_8_st.setText(str(data[8]))
        else:
                self.messagebox("Сообщение", "Нет записи в БД")


    def Delete_Students(self):
        ID = self.lineEdit_2_st.text()
        sql = 'DELETE FROM students WHERE ID=?'
        self.cur.execute(sql, [(ID)])
        self.db.commit()
        self.loaddata()
        self.Clear()

            
    def Clear(self):
        self.lineEdit_2_st.setText("") 
        self.lineEdit_3_st.setText("")
        self.lineEdit_4_st.setText("")
        self.lineEdit_st.setText("")
        self.lineEdit_6_st_2.setText("")
        self.lineEdit_6_st.setText("")
        self.lineEdit_5_st.setText("")
        self.lineEdit_7_st.setText("")
        self.lineEdit_8_st.setText("")

        self.lineEdit_seatch_st.setText("")

    def clear_table(self):
        
        self.table_st.setRowCount(0)


    def Update_Students(self):
        ID = self.lineEdit_2_st.text()
        if(ID):
            ID = self.lineEdit_2_st.text()
            surname = self.lineEdit_3_st.text()
            name = self.lineEdit_4_st.text()
            patronymic = self.lineEdit_st.text()
            gender = self.lineEdit_6_st_2.text() 
            number = self.lineEdit_6_st.text()
            id_groupe = self.lineEdit_5_st.text()
            mail = self.lineEdit_7_st.text()
            phone = self.lineEdit_8_st.text()
            
            self.cur.execute('''
                                UPDATE students SET ID=?, surname=?, name=?, patronymic=?,  gender=?, number=?, id_groupe=?,  mail=?,  phone=? WHERE ID=?
                                ''',(ID, surname, name,  patronymic, gender,  number, id_groupe, mail, phone,ID))
            self.db.commit()
            self.Clear()
            self.messagebox("Сообщение", "Запись обновлена")
            self.loaddata()
        else:
            self.messagebox("Сообщение", "Запись не обновлена")

    def loaddata(self):
        self.cur.execute('SELECT * FROM students LIMIT 300')
        rows = self.cur.fetchall()
        self.table_st.setRowCount(len(rows))
        for row_num, row_data in enumerate(rows):
            for col_num, data in enumerate(row_data):
                self.table_st.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))
        self.table_st.resizeColumnsToContents()


        
def main():
    app = QApplication(sys.argv)
    window = MainAppStudents()
    window.setFixedSize(1702, 903) 
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

