from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

timepair_ui, _ = loadUiType('timepair.ui')

class MainFormTimePair(QMainWindow, timepair_ui):
    def __init__(self, parent=None):
        super(MainFormTimePair, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TimePair")
        
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Start Time", "End Time"])
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/OneDrive/Рабочий стол/Code_rename/photo/clock.jpg'))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainFormTimePair()
    mainWin.show()
    sys.exit(app.exec_())

