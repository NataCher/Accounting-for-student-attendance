from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

menu_ui, _ = loadUiType('menu.ui')
groupe_ui, _ = loadUiType('groupe.ui')
shedule_ui, _= loadUiType('shedule.ui')
teachers_ui, _= loadUiType('teachers.ui')
subjects_ui, _= loadUiType('subjects.ui')
journal_ui, _= loadUiType('journal.ui')
students_ui, _= loadUiType('students.ui')
timepair_ui, _ = loadUiType('timepair.ui')


#====================================================================
#====================================================================

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
        pass



#====================================================================
#====================================================================

class MainAppJournal(QMainWindow, journal_ui):
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

        self.shedule_btn.clicked.connect(self.open_Journal_form)

    def open_Journal_form(self):
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

        pass
#====================================================================
#====================================================================

class MainAppMenu(QMainWindow, menu_ui):
    def __init__(self, parent=None):
        super(MainAppMenu, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/menu-bar.png'))
        
        self.groupe.clicked.connect(self.open_groupe_form)

        self.btn_students.clicked.connect(self.open_students_form)

        self.teacher_btn.clicked.connect(self.open_teachers_form)

        self.subjects_btn.clicked.connect(self.open_subjects_form)

        self.journal_btn.clicked.connect(self.open_journal_form)

    def open_groupe_form(self):
        self.close()
        self.groupe_form = MainAppGroupe()
        self.groupe_form.show()

    def open_students_form(self):
        self.close()
        self.students_form = MainAppStudents()
        self.students_form.show()

    def open_teachers_form(self):
        self.close()
        self.teachers_form = MainAppTeachers()
        self.teachers_form.show()

    def open_subjects_form(self):
        self.close()
        self.subjects_form = MainAppSubjects()
        self.subjects_form.show()

    def open_journal_form(self):
        self.close()
        self.subjects_form = MainAppJournal()
        self.subjects_form.show()

    pass
#====================================================================
#====================================================================

class MainAppShedule(QMainWindow, shedule_ui):
    
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
    pass
        
#====================================================================
#====================================================================

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


    pass

#====================================================================
#====================================================================

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

    pass

#====================================================================
#====================================================================

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
            self.loaddata() 
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
        
        pass

#====================================================================
#====================================================================

class MainFormTimePair(QMainWindow, timepair_ui):
    def __init__(self, parent=None):
        super(MainFormTimePair, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TimePair")
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/clock.jpg'))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Start Time", "End Time"])

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pairs")
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        
        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()
        cursor.close()
        connection.close()
    
