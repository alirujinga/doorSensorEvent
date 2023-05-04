'''
* \file mainPannel.py
* \author Matthew Li
* \copyright Arxtron Technologies Inc.. All Rights Reserved.
* \date 1/25/2023 9:43:33 AM
* \brief A short description.
*
* A longer description.
*
* Version     |   Date        |   Author          |   Description
* ------------|---------------|-------------------|-----------------------------
* 0.0.0       | 1/25/2023  | Matthew Li       | This version can support basic function, log in, log out, read CSV file, search result based on name and date
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtGui import *
import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime as dt
import os
import calendar
import re
'''
Class DataFrame model

Used to transfer dataframe to QAbstractTableModel. the index must increase from 0 and must no gap add one more.

initial input dataframe

example:

newDataFrameModel = DataframeModel(df)

df is a dataframe
'''

'''
create globle function here 

'''
class DataFrameWindow(QtWidgets.QMainWindow):
    def __init__(self,df,name):
        super().__init__()
        self.df = df
        self.name = name
        self.initUI()
        self.resize(1300,800)


    def initUI(self):
        self.setWindowTitle(self.name)
        self.table = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table)

        # Set table properties
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        # self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Populate table with data
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                item = QtWidgets.QTableWidgetItem(str(self.df.iloc[i, j]))
                self.table.setItem(i, j, item)
        if len(self.df.columns)>7:
            for i in range(len(self.df.columns)):
                self.table.setColumnWidth(i, 220)
        else:
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


#class used to transfer dataframe to QAbstractTableModel. the index must increase from 0 and must no gap add one more.
class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles


class CustomDialog(QDialog):
    def __init__(self,message):
        super().__init__()
        dlg = QDialog()
        dlg.setFixedWidth(300)
        dlg.setFixedHeight(60)
        messageLabel = QLabel(message, dlg)
        messageLabel.move(20, 20)
        dlg.setWindowTitle(message)
        dlg.exec_()

'''
Class Query window

This is subwidow for main window

when Log in then jump out Query window

initial with dataframe input
'''
class QueryWindow(QMainWindow):

    def __init__(self,DataFrame):
        super().__init__()
        self.df = DataFrame

        #initial query condition
        self.selectedName = None
        self.selectedStartTime = None
        self.selectedEndTime = None

        # setting title
        self.setWindowTitle("Query Window")

        # setting geometry
        self.setGeometry(300, 200, 450, 700)

        # calling initial method
        self.initDateSelector()
        self.initNameList()
        self.initButton()
        self.initMenuBar()



    def initMenuBar(self):
        self.menuBar1 = self.menuBar()
        # self.menuBar1.setGeometry(QRect(0, 0, 800, 800))
        self.menuBar1.setObjectName("menuBar")  #main menu bar
        self.menu1 = self.menuBar1.addMenu('File') #first menu
        self.menu2 = self.menuBar1.addMenu('Event')  # second menu
        self.menu3 = self.menuBar1.addMenu('DateSelect')  # second menu

        '''intial submenu:'''

        #initial load new csv file sub menu
        loadNewCSVaction = QAction("ReadNewCSV", self.menu1) #create one action to first menu
        loadNewCSVaction.setShortcut('Ctrl+R') #add short cut for loadNewCSVaction
        self.menu1.addAction(loadNewCSVaction) #add loadNewCSVaction to menu1
        loadNewCSVaction.triggered.connect(self.loadNewCSVaction) #connect loadNewCSVaction's function

        #initial tool's show last event menu.
        lastEvent = QAction("ChooseLastEvent", self.menu2) #create one action to first menu
        lastEvent.setShortcut('Ctrl+L') #add short cut for loadNewCSVaction
        self.menu2.addAction(lastEvent) #add loadNewCSVaction to menu1
        lastEvent.triggered.connect(self.showLastEventForEachOne) #connect loadNewCSVaction's function


        LastDay = QAction("LastDay", self.menu3) #create one action to first menu
        LastDay.setShortcut('Ctrl+L+D') #add short cut for loadNewCSVaction
        self.menu3.addAction(LastDay) #add loadNewCSVaction to menu1
        LastDay.triggered.connect(self.setOneDayBefore) #connect loadNewCSVaction's function

        LastWeek = QAction("LastWeek", self.menu3) #create one action to first menu
        LastWeek.setShortcut('Ctrl+L+W') #add short cut for loadNewCSVaction
        self.menu3.addAction(LastWeek) #add loadNewCSVaction to menu1
        LastWeek.triggered.connect(self.setOneWeekBefore) #connect loadNewCSVaction's function

        LastMonth = QAction("LastFourWeeks", self.menu3) #create one action to first menu
        LastMonth.setShortcut('Ctrl+L+M') #add short cut for loadNewCSVaction
        self.menu3.addAction(LastMonth) #add loadNewCSVaction to menu1
        LastMonth.triggered.connect(self.setFourWeekBefore) #connect loadNewCSVaction's function

        LastFiveWeek = QAction("LastFiveWeeks", self.menu3) #create one action to first menu
        LastFiveWeek.setShortcut('Ctrl+L+M') #add short cut for loadNewCSVaction
        self.menu3.addAction(LastFiveWeek) #add loadNewCSVaction to menu1
        LastFiveWeek.triggered.connect(self.setFiveWeekBefore) #connect loadNewCSVaction's function

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)  # connect right click menu, current not use

    #initial date selector
    def initDateSelector(self):
        self.datetimeeditStart = QDateTimeEdit(self)
        self.datetimeeditEnd = QDateTimeEdit(self)
        self.datetimeeditStart.setGeometry(30, 50, 150, 35)
        self.datetimeeditEnd.setGeometry(200, 50, 150, 35)
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),-7))
        self.datetimeeditEnd.setDate(QDate.currentDate())

    #initial query winodow's button
    def initButton(self):
        # self.lastOnedaySelectButton = QPushButton("Last day",self)
        # self.lastOneWeekSelectButton = QPushButton("Last week",self)
        # self.lastOneMonthSelectButton = QPushButton("Last month",self)
        self.query = QPushButton("Query",self)

        self.query.clicked.connect(self.queryResult)

        #set query button's style
        self.query.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
        # self.lastOnedaySelectButton.clicked.connect(self.setOneDayBefore)
        # self.lastOneWeekSelectButton.clicked.connect(self.setOneWeekBefore)
        # self.lastOneMonthSelectButton.clicked.connect(self.setOneMonthBefore)

        # self.lastOnedaySelectButton.setGeometry(300, 100, 100, 30)
        # self.lastOneWeekSelectButton.setGeometry(300, 200, 100, 30)
        # self.lastOneMonthSelectButton.setGeometry(300, 300, 100, 30)
        self.query.setGeometry(300,600,100,50)

    # create nameList Component
    def initNameList(self):
        # creating a QListWidget
        self.list_widget = QListWidget(self)
        # setting geometry to it
        self.list_widget.setGeometry(30, 120, 220, 550)
        nameList = {}
        blankName = QListWidgetItem("All")
        nameList["All"] = blankName
        self.list_widget.addItem(blankName)
        names = pd.read_csv('//192.168.1.6/Door_Controller$/users.csv', header=None)[0]
        for name in names:
            item = QListWidgetItem(name)
            nameList[name] = item  # add QList to dict
            self.list_widget.addItem(item)

        # names = self.df[["First Name","Last Name"]]
        # colomn =names.shape[0]
        # for i in range(colomn):
        #     name = names.iloc[i]['First Name']+' '+names.iloc[i]['Last Name']
        #     if name not in nameList:
        #         item = QListWidgetItem(name)
        #         nameList[name] = item  #add QList to dict
        #         self.list_widget.addItem(item)


        # setting drag drop mode
        self.list_widget.setDragDropMode(QAbstractItemView.DragDrop)
        # self.list_widget.itemClicked.connect(self.printName)  # connect itemClicked to Clicked method
        self.list_widget.itemPressed.connect(self.printName)  # connect itemClicked to Clicked method
    #click query button then get query result(result is dataFrame fomat)
    def queryResult(self):
        self.selectedStartTime = '{0}/{1}/{2}'.format(self.datetimeeditStart.date().month(),
                                                      self.datetimeeditStart.date().day(),
                                                      self.datetimeeditStart.date().year())
        self.selectedEndTime = '{0}/{1}/{2}'.format(self.datetimeeditEnd.date().month(),
                                                    self.datetimeeditEnd.date().day(),
                                                    self.datetimeeditEnd.date().year())

        self.selectedStartTime = dt.strptime(self.selectedStartTime, "%m/%d/%Y")
        self.selectedEndTime = dt.strptime(self.selectedEndTime, "%m/%d/%Y")

        if self.selectedName != "All":
            try:
                selectedFirstName, selectedLastName = self.selectedName.split(' ')
                self.selectedDf = self.df[self.df["First Name"] == selectedFirstName]
                self.selectedDf = self.df[self.df["Last Name"] == selectedLastName]
            except Exception as e:
                print(str(e))
                self.selectedDf = self.df.copy()
        else:
            self.selectedDf = self.df.copy()
        self.selectedDf.reset_index(drop=True, inplace=True)
        try:
            self.selectedDf = self.transferStrToDate(self.selectedDf)
        except Exception as e:
            print(e)
        mask = (self.selectedDf["Date"] > self.selectedStartTime) & (self.selectedDf["Date"] <= self.selectedEndTime)
        self.selectedDf = self.selectedDf[mask]
        self.selectedDf.reset_index(drop=True, inplace=True)
        # print(self.selectedDf)
        # selectedDf = self.df[self.df["Date"] > self.selectedStartTime]
        # selectedDf.reset_index(drop=True, inplace=True)
        self.selectedDf = self.shortEvent(self.selectedDf)
        self.selectedDf = self.transferDateToStr(self.selectedDf)
        self.queryWindow = self.showTables(self.selectedDf) #refresh table shows

    #add in Dataframe and show on the screen
    def showTables(self,df):
        # creating a table view
        # column = df.shape[1]
        # self.tableView = QTableView()
        # self.tableView.setWindowTitle(self.selectedName)
        # self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tableView.setObjectName("tableView")
        # self.tableView.resize(1600,800)
        # # self.tableView.horizontalHeader().setStretchLastSection(True) #fill all window
        # # for i in range(column):
        # #     self.tableView.setColumnWidth(i,1000) #set all column to same size
        # for i, column in enumerate(df.columns):
        #     self.tableView.setColumnWidth(i, 200)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        # # self.tableView = QtWidgets.QTableWidget()
        # # self.setCentralWidget(self.tableView)
        # #
        # # # Set table properties
        # # self.tableView.setRowCount(len(df))
        # # self.tableView.setColumnCount(len(df.columns))
        # # self.tableView.setHorizontalHeaderLabels(df.columns)
        # # self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # #
        # # # Populate table with data
        # # for i in range(len(df)):
        # #     for j in range(len(df.columns)):
        # #         item = QtWidgets.QTableWidgetItem(str(df.iloc[i, j]))
        # #         self.tableView.setItem(i, j, item)
        # #         self.tableView.setColumnWidth(j, 500)


        self.tableView = DataFrameWindow(df,self.selectedName)

        self.ResultMenuBar = QMenuBar(self.tableView)
        self.ResultMenuBar.resize(20,10)


        file = self.ResultMenuBar.addMenu("File")
        file.resize(20,10)
        save = QAction("Save", self)
        save.setShortcut("Shift+S")
        file.addAction(save)
        save.triggered.connect(self.saveFileDialog)


        # self.tableView.selectionModel().selectionChanged.connect(self.getIndex)
        # model = DataFrameModel(df)
        # try:
        #     self.tableView.setModel(model)
        # except Exception as e:
        #     print(e)
        self.tableView.show()

    # @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    # def getIndex(self, selected, deselected):
    #     print("=====Selected=====")
    #     for ix in selected.indexes():
    #         print(ix.row(), ix.column())
    #     print("=====Deselected=====")
    #     for ix in deselected.indexes():
    #         print(ix.row(), ix.column())

    def rightMenuShow(self):
        rightMenu = QMenu(self.menuBar1)

        self.chooseOneDay = QAction('oneDay')
        self.chooseOneDay.setObjectName("oneDay")
        self.chooseOneDay.setText(QCoreApplication.translate("MainWindow", "LastDay"))
        self.chooseOneDay.triggered.connect(self.showOneDayBefore)

        self.chooseOneWeek = QAction('oneWeek')
        self.chooseOneWeek.setObjectName("oneWeek")
        self.chooseOneWeek.setText(QCoreApplication.translate("MainWindow", "LastWeek"))
        self.chooseOneWeek.triggered.connect(self.showOneWeekBefore)

        self.chooseOneMonth = QAction('oneMonth')
        self.chooseOneMonth.setObjectName("oneMonth")
        self.chooseOneMonth.setText(QCoreApplication.translate("MainWindow", "LastFourWeeks"))
        self.chooseOneMonth.triggered.connect(self.showFourWeekBefore)

        self.chooseFiveWeek = QAction('FiveWeek')
        self.chooseFiveWeek.setObjectName("oneMonth")
        self.chooseFiveWeek.setText(QCoreApplication.translate("MainWindow", "LastFiveWeeks"))
        self.chooseFiveWeek.triggered.connect(self.showFiveWeekBefore)

        self.showLastEvent = QAction('PersonalPage')
        self.showLastEvent.setObjectName("showPersonPage")
        self.showLastEvent.setText(QCoreApplication.translate("MainWindow", "showPersonPage"))
        self.showLastEvent.triggered.connect(self.showPersonPage)


        rightMenu.addAction(self.chooseOneDay)
        rightMenu.addAction(self.chooseOneWeek)
        rightMenu.addAction(self.chooseOneMonth)
        rightMenu.addAction(self.chooseFiveWeek)
        rightMenu.addAction(self.showLastEvent)
        # subM=rightMenu.addMenu("subMenu")
        # self.ac1 = QAction('hhjh')
        # subM.addAction(self.ac1)
        # self.ac1.triggered.connect(self.test)

        rightMenu.exec_(QCursor.pos())

    #used to double check which name seleted
    def printName(self,item):
        self.selectedName = item.text()
        # QMessageBox.information(self, "Selected Name", "You select: " + item.text())

    #used to transfer string format for date to date format
    def transferStrToDate(self,df):
        line = df.shape[0]
        for i in range(0,line):
            dateTime = df["Date"][i]+" "+df["Time"][i].split(' ')[0]
            try:
                Date = dt.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                if e:
                    # Date = dt.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
                    print(e)
            df._set_value(i, "Date", Date) #use _set_value to reset one item in dataframe i: ith row; "Date": column ; Date: new data(Value)
        return df

    #used to transfer string format for date to date format
    def transferDateToStr(self,df):
        line = df.shape[0]
        for i in range(0,line):
            dateTime = df["Date"][i]
            Date = dt.strftime(dateTime, "%Y-%m-%d %H:%M:%S").split(' ')[0]
            df._set_value(i, "Date", Date) #use _set_value to reset one item in dataframe i: ith row; "Date": column ; Date: new data(Value)
        return df

    #used to transfer string format for date to date format
    def transferDateForPerson(self,df):
        line = df.shape[0]
        for i in range(0,line):
            dateTime = df["Date"][i]
            dayOfWeek = calendar.day_name[dateTime.weekday()]
            dateTime = str(dateTime).split(' ')[0]
            Date = dateTime+'('+dayOfWeek+')'
            df._set_value(i, "Date", Date) #use _set_value to reset one item in dataframe i: ith row; "Date": column ; Date: new data(Value)
        return df


    #used to short spell event, event in csv file is too long
    def shortEvent(self,df):
        line = df.shape[0]
        lineDelete = []
        for i in range(0, line):
            event = df["Event Details"][i]
            if "Exit" in event:
                if "Front-Door" in event:
                    df._set_value(i, "Event Details", "Exit, Front-Door")
                else:
                    df._set_value(i, "Event Details", "Exit, Back-Door")
            if "Entered" in event:
                if "Front-Door" in event:
                    df._set_value(i, "Event Details", "Enter, Front-Door")
                else:
                    df._set_value(i, "Event Details", "Enter, Back-Door")
            if "Access" in event:
                lineDelete.append(i)
        df = df.drop(lineDelete)  #delete all access message
        df.reset_index(drop=True, inplace=True)
        return df

    #set query period to one day before
    def setOneDayBefore(self):
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -1))
        self.datetimeeditEnd.setDate(QDate.currentDate())
    # set query period to one week before
    def setOneWeekBefore(self):
        #self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -7))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-7))

    # set query period to one month before
    def setFourWeekBefore(self):
        # self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -30))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-28))

    def setFiveWeekBefore(self):
        # self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -30))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-35))


    def showOneDayBefore(self):
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -1))
        self.datetimeeditEnd.setDate(QDate.currentDate())
        self.showPersonPage()
    # set query period to one week before
    def showOneWeekBefore(self):
        #self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -7))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-7))
        self.showPersonPage()

    # set query period to one month before
    def showFourWeekBefore(self):
        # self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -30))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-28))
        self.showPersonPage()
    def showFiveWeekBefore(self):
        # self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(), -30))
        currentDate = QDate.currentDate()
        currentDayofWeek = -1*(currentDate.dayOfWeek()-1)
        self.datetimeeditEnd.setDate(QDate.addDays(currentDate,currentDayofWeek))
        self.datetimeeditStart.setDate(QDate.addDays(QDate.currentDate(),currentDayofWeek-35))
        self.showPersonPage()

    #show last event for each person
    def showLastEventForEachOne(self):
        lastEventSet = {}
        try:
            self.lastEventDf = self.transferStrToDate(self.df)
        except Exception as e:
            print(e)
        row = self.lastEventDf.shape[0]
        for i in range(row):
            oneRecord = self.lastEventDf.iloc[i] #get one row
            searchName = oneRecord["First Name"]+' '+oneRecord["Last Name"]
            if searchName not in lastEventSet:
                lastEventSet[searchName] = oneRecord
            else:
                if oneRecord["Date"]>lastEventSet[searchName]["Date"]:
                    lastEventSet[searchName] = oneRecord
        self.lastEventDf = ''
        for eachItem in lastEventSet:
            if len(self.lastEventDf) == 0:
                firstBuild = {}
                for i in lastEventSet[eachItem].keys():
                    firstBuild[i] = lastEventSet[eachItem][i]
                self.lastEventDf = pd.DataFrame([firstBuild],columns=firstBuild.keys()) #transfer dict to dataFrame, column name is dict's key name
            else:
                self.lastEventDf = self.lastEventDf.append(lastEventSet[eachItem].transpose(),ignore_index = True)
        self.lastEventDf = self.lastEventDf.sort_values(by="Date", ascending=True,ignore_index=True)
        print(self.lastEventDf)



        self.selectedDf = self.shortEvent(self.lastEventDf)
        self.selectedName = "Each emplyee's last event"
        self.queryWindow = self.showTables(self.selectedDf)  # refresh table shows


    def showPersonPage(self):
        # self.selectedStartTime = '{0}/{1}/{2}'.format(self.datetimeeditStart.date().month(),self.datetimeeditStart.date().day(),self.datetimeeditStart.date().year())
        # self.selectedEndTime = '{0}/{1}/{2}'.format(self.datetimeeditEnd.date().month()+'/'+self.datetimeeditEnd.date().day()+'/'+self.datetimeeditEnd.date().year())
        self.selectedStartTime = '{0}/{1}/{2}'.format(self.datetimeeditStart.date().month(),
                                                      self.datetimeeditStart.date().day(),
                                                      self.datetimeeditStart.date().year())
        self.selectedEndTime = '{0}/{1}/{2}'.format(self.datetimeeditEnd.date().month(),
                                                    self.datetimeeditEnd.date().day(),
                                                    self.datetimeeditEnd.date().year())

        self.selectedStartTime = dt.strptime(self.selectedStartTime, "%m/%d/%Y")
        self.selectedEndTime = dt.strptime(self.selectedEndTime, "%m/%d/%Y")

        if self.selectedName != "All":
            selectedFirstName,selectedLastName = self.selectedName.split(' ')
            self.selectedDf = self.df[self.df["First Name"] == selectedFirstName]
            self.selectedDf = self.df[self.df["Last Name"] == selectedLastName]
        else:
            self.selectedDf = self.df
        self.selectedDf.reset_index(drop=True, inplace=True)
        try:
            self.selectedDf = self.transferStrToDate(self.selectedDf)
        except Exception as e:
            print(e)
        mask = (self.selectedDf["Date"] > self.selectedStartTime) & (self.selectedDf["Date"] <= self.selectedEndTime)
        self.selectedDf = self.selectedDf[mask]
        self.selectedDf.reset_index(drop=True, inplace=True)
        # print(self.selectedDf)
        # selectedDf = self.df[self.df["Date"] > self.selectedStartTime]
        # selectedDf.reset_index(drop=True, inplace=True)
        self.selectedDf = self.shortEvent(self.selectedDf)
        self.selectedDf = self.selectedDf.sort_values(by="Date", ascending=True)
        self.selectedDf = self.transferDateForPerson(self.selectedDf)

        eachDayFrame = {}
        row = self.selectedDf.shape[0]
        for i in range(row):
            date = self.selectedDf.iloc[i]["Date"]
            if date not in eachDayFrame:
                eachDayFrame[date] = []
                eachDayFrame[date].append('['+self.selectedDf.iloc[i]["Time"]+']'+self.selectedDf.iloc[i]["Event Details"])
            else:
                eachDayFrame[date].append('['+self.selectedDf.iloc[i]["Time"]+']'+self.selectedDf.iloc[i]["Event Details"])
        eachDayFrame = self.transferToSameSizeForDict(eachDayFrame)
        eachDayFrame,wholeWorktime,wholeStaytime = self.calculateWorkingTime(eachDayFrame)
        self.selectedDf = pd.DataFrame(eachDayFrame)  #transfer dict to dataframe if dict key is a list
        self.selectedName = '['+self.selectedName+']'+', TE:'+ str(round(wholeWorktime,2))+', TD:'+str(round(wholeStaytime,2))
        self.queryWindow = self.showTables(self.selectedDf)  # refresh table shows

    def calculateWorkingTime(self,dict):
        wholeWorkTime = 0
        wholeStayTime = 0
        for eachKey in dict:
            lastEvent = ''
            workingTime = 0.0 #not include work out for lunch
            stayTime = 0.0 #The time between First enter office and go home
            try:
                for eachItem in dict[eachKey]:
                    if "Enter" in lastEvent:
                        lastEventTime = re.findall(r'[[](.*?)[]]', lastEvent)[0]
                        if 'Exit' in eachItem:
                            EventTime = re.findall(r'[[](.*?)[]]', eachItem)[0]
                            workingTime += self.calculateTimeBetweenTwoTimeStamp(lastEventTime,EventTime)
                    lastEvent = eachItem
                firstEnter = re.findall(r'[[](.*?)[]]', dict[eachKey][0])[0]
                for j in range(len(dict[eachKey])-1,-1,-1):
                    if dict[eachKey][j] != '':
                        lastExit = re.findall(r'[[](.*?)[]]', dict[eachKey][j])[0]
                        break
                if len(dict[eachKey])>1:
                    stayTime = self.calculateTimeBetweenTwoTimeStamp(firstEnter,lastExit)
                else:
                    stayTime = 0.0
            except Exception as e:
                print(str(e))
            dict[eachKey].append(round(workingTime,2))
            wholeWorkTime+=workingTime
            dict[eachKey].append(round(stayTime,2))
            wholeStayTime+=stayTime
        return dict,wholeWorkTime,wholeStayTime

    def calculateTimeBetweenTwoTimeStamp(self,time1,time2): #The time must in same day and must be HH:MM:SS format
        time1 = time1.split(':')
        time2 = time2.split(':')
        timeGap = int(time2[0])-int(time1[0])+(int(time2[1])-int(time1[1]))/60
        return timeGap



    def transferToSameSizeForDict(self,dict):
        maxSize = 0
        for i in dict:
            size = len(dict[i])
            if size>maxSize:
                maxSize = size

        for i in dict:
            for j in range(maxSize-len(dict[i])):
                dict[i].append('')
        return dict


    def loadNewCSVaction(self): #used to select CSV file
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            if fileName.split('.')[-1] != "csv":
                Qdialog = CustomDialog("wrong file format, must be csv file")
            else:
                self.CSVpath = fileName
                df1 = pd.read_csv(self.CSVpath)
                self.df = df1
                QMessageBox.information(self, "Success", "Success read new CSV File")
                print(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;csv Files (*.csv)", options=options)
        if fileName:
            print(fileName)
            if fileName.split('.')[-1] != 'csv':
                fileName = fileName+'.csv'
            try:
                self.selectedDf.to_csv(fileName)
                QMessageBox.information(self,"Sucessfully","File saved!")
            except Exception as e:
                print(e)
        else:
            pass
            # QMessageBox.information(self,"NO NAME ERROR","NO NAME INPUT")


    def logFunc(self,logMessage):
        logMessage = str(logMessage)+'\n'
        with open("QueryWindowError.log", 'a') as f:
            logMessage = '[' + str(dt.now()) + ']' + logMessage
            f.write(logMessage)


    def testFunction(self):
        print("function called")
        self.testWindow = DataFrameWindow(self.df)
        self.testWindow.show()



'''
This is class main window
covered login and log out and read csv file
'''
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Pannel")
        #define main window's self attributes
        self.component = []

        #define new sub window here
        self.NameCheckList = None

        #define initial function
        self.initUI()
        self.initButton()
        self.initQtable()
        self.initLabel()
        # self.initDateSelector()
        # self.initCheckList()
        self.initComponent()
        self.initSystermSetting()


    def initUI(self): #initial main window size and position
        self.setGeometry(50,50,540,300)

    def initButton(self): #initial all button for main window
        self.loginButton = QPushButton("log in", self)
        self.logoutButton = QPushButton("log out", self)
        self.readCSVButton = QPushButton("QueryWindow", self)
        # self.readCSVButton.move(100,0)
        # self.logoutButton.move(0,0)
        self.loginButton.setGeometry(0,0,120,50)
        self.logoutButton.setGeometry(0,0,120,50)
        self.readCSVButton.setGeometry(130,0,120,50)
        self.readCSVButton.setVisible(False)
        self.logoutButton.setVisible(False)
        # self.button.setGeometry(0,0,30,20)
        self.loginButton.clicked.connect(self.login)
        self.readCSVButton.clicked.connect(self.openQueryWindow)
        self.logoutButton.clicked.connect(self.logout)
        self.component.append(self.logoutButton)
        self.component.append(self.readCSVButton)

    def initLabel(self):
        # creating label
        self.label = QLabel(self)
        # loading image
        self.pixmap = QPixmap('arxtron.jpg')
        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.move(250,0)


    def initComponent(self): #set which component need to visible when first run
        for oneItem in self.component:
            oneItem.setVisible(False)

    def initInfo(self): #initial current input account
        self.username = None
        self.password = None
        self.w = None  # No external window yet.
        # self.setCentralWidget(self.button)
        self.CSVpath = None
    def initSystermSetting(self):
        self.SystermSetting = pd.read_csv('//192.168.1.6/Door_Controller$/systermSetting.csv')
        userListPath = self.SystermSetting['userListPath'].iloc[0]
        self.users = pd.read_csv(userListPath)

    def initQtable(self): #initial first Qtable which is used to show all items in CSV
        self.tableView = QTableView()
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableView.setObjectName("tableView")
        self.tableView.setWindowTitle("All Result")

    def showNameCheckList(self,df): #used to call subwindow for Query window
        self.NameCheckList = QueryWindow(df)
        self.NameCheckList.show()

    def openQueryWindow(self): #used to select CSV file
        self.showNameCheckList(self.df1) #show name check list subwindow

    def openFileNameDialog(self): #used to select CSV file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            if fileName.split('.')[-1] != "csv":
                Qdialog = CustomDialog("wrong file format, must be csv file")
            else:
                self.CSVpath = fileName
                df1 = pd.read_csv(self.CSVpath)
                # model = DataFrameModel(df1)
                self.showNameCheckList(df1) #show name check list subwindow
                # self.tableView.setModel(model)
                # self.tableView.show()
                print(fileName)

    def login(self): #log in function
        self.username, self.ok = QInputDialog.getText(self, 'Authentication', 'Input username')
        self.password, self.ok = QInputDialog.getText(self, 'Authentication', 'Input password',QLineEdit.Password)
        self.CSVpath = self.SystermSetting['serverFilePath'].iloc[0]

        # self.CSVpath = self.SystermSetting['serverFilePath'].iloc[0]
        # model = DataFrameModel(df1)

        # self.tableView.setModel(model)
        # self.tableView.show()
        user = self.users
        password = user[user['Username']==self.username]
        if password.size >0:
            password = password['Password'].iloc[0]
        else:
            password = None
        if (password == self.password): #if log in, vanish button
            self.loginButton.setVisible(False)
            for item in self.component:
                item.setVisible(True)
            try:
                self.df1 = pd.read_csv(self.CSVpath)
                self.df1 = self.df1.dropna()
                QMessageBox.information(self, "Success", "Success read eventfile")
            except Exception as e:
                QMessageBox.information(self, "Fail", "Fail to read eventfile")
        else:
            Qdialog = CustomDialog("wrong username or password")

        # self.showNameCheckList(df1)  # show name check list subwindow

    def logout(self): #log out function
        self.loginButton.setVisible(True)
        for item in self.component:
            item.setVisible(False)
        try:
            if self.NameCheckList:
                if  self.NameCheckList.tableView:
                    self.NameCheckList.tableView.close()
                self.NameCheckList.close()
        except Exception as e:
            print(str(e))


#the enter of function
if __name__ == "__main__":
    try:
        print(os.getcwd())
        app = QApplication(sys.argv)
        w = MainWindow()
        w.show()
        app.exec()
    except Exception as e:
        with open("re.log",'w') as f:
            f.write(e)
