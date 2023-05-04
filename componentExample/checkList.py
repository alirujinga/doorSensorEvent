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

        self.button = QPushButton("add",self)
        self.button.clicked.connect(self.add)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()



    def add(self):
        item = QListWidgetItem("A")
        self.list_widget.addItem(item)

    # method for components
    def UiComponents(self):
        # creating a QListWidget
        self.list_widget = QListWidget(self)

        # setting geometry to it
        self.list_widget.setGeometry(50, 70, 100, 300)

        list = ['a','b','c','d','e','f','a','b']
        # list widget items
        listDict = {}
        for i in list:
            if i not in listDict:
                item = QListWidgetItem(i)
                self.list_widget.addItem(item)
                listDict[i] = item
        # item1 = QListWidgetItem("A")
        # item2 = QListWidgetItem("B")
        # item3 = QListWidgetItem("C")
        #
        # # adding items to the list widget
        # list_widget.addItem(item1)
        # list_widget.addItem(item2)
        # list_widget.addItem(item3)

        # setting drag drop mode
        self.list_widget.setDragDropMode(QAbstractItemView.DragDrop)

        # creating a label
        label = QLabel("GeeksforGeeks", self)

        # setting geometry to the label
        label.setGeometry(230, 80, 280, 80)

        # making label multi line
        label.setWordWrap(True)


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem


class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    listWidget = QListWidget()
    window.setWindowTitle("Demo for QListWidget")

    QListWidgetItem("Geeks", listWidget)
    QListWidgetItem("For", listWidget)
    QListWidgetItem("Geeks", listWidget)

    listWidgetItem = QListWidgetItem("GeeksForGeeks")
    listWidget.addItem(listWidgetItem)

    window_layout = QVBoxLayout(window)
    window_layout.addWidget(listWidget)
    window.setLayout(window_layout)

    window.show()

    sys.exit(app.exec_())