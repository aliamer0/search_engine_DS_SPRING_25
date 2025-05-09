from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 400, 261, 81))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start_crawling)  # Connect button click to start_crawling function

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 240, 441, 91))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 270, 131, 20))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Distributed Crawler"))
        self.pushButton.setText(_translate("MainWindow", "Start Crawling and Indexing"))
        self.label.setText(_translate("MainWindow", "Enter the URL"))

    def start_crawling(self):
        url = self.lineEdit.text()  # Get the URL from the text box
        if url:
            # Here you can call your subprocess to start the crawling, indexing, and master process
            # Replace the command with your own path and parameters
            subprocess.Popen(["mpiexec", "-n", "6", "python", "-m", "Master.master_node", url])
        else:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please enter a URL to start the process.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
