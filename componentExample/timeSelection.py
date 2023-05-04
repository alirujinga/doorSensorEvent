# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 500, 400)

        # calling method
        self.UiComponents()


        self.button = QPushButton("set date",self)
        self.button.clicked.connect(self.printTime)
        # showing all the widgets
        self.show()



    # method for components


    def printTime(self):

        print( self.datetimeedit.dateTime())
        print(self.datetimeeditEnd.dateTime())
    def UiComponents(self):
        # creating a QDateTimeEdit widget
        self.datetimeedit = QDateTimeEdit(self)
        self.datetimeeditEnd = QDateTimeEdit(self)

        # setting geometry
        self.datetimeedit.setGeometry(100, 100, 150, 35)
        self.datetimeeditEnd.setGeometry(200, 200, 150, 35)
        # QDateTime
        dt = QDateTime(2020, 10, 10, 21, 30)

        # setting date time to datetimeedit
        self.datetimeedit.setDateTime(dt)

        # creating a label
        label = QLabel("GeeksforGeeks", self)

        # setting geometry to the label
        label.setGeometry(100, 160, 200, 60)

        # making label multi line
        label.setWordWrap(True)

        # getting current datetime
        value = self.datetimeedit.dateTime()

        # setting text to label
        label.setText("DateTime : " + str(value))


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())