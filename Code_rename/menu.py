from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

from dopclass import MainAppStudents
from dopclass import MainAppGroupe
from dopclass import MainAppTeachers
from dopclass import MainAppSubjects
from dopclass import MainAppJournal


menu_ui, _= loadUiType('menu.ui')
groupe_ui, _ = loadUiType('groupe.ui')
students_ui, _= loadUiType('students.ui')
teachers_ui, _= loadUiType('teachers.ui')
subjects_ui, _= loadUiType('subjects.ui')
journal_ui, _= loadUiType('journal.ui')

class MainAppMenu(QMainWindow,menu_ui):
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
        self.journal_form = MainAppJournal()
        self.journal_form.show()
     


def main():
    app = QApplication(sys.argv)
    window = MainAppMenu()
    window.setFixedSize(890, 545) 
    window.show()
    app.exec_()

if __name__ == '__main__':
     main()
