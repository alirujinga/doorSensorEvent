from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.table = QtWidgets.QTableWidget(6, 6)
        self.setCentralWidget(self.table)
        self.table.selectionModel().selectionChanged.connect(
            self.on_selectionChanged
        )

    @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        print("=====Selected=====")
        for ix in selected.indexes():
            print(ix.row(), ix.column())
        print("=====Deselected=====")
        for ix in deselected.indexes():
            print(ix.row(), ix.column())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())