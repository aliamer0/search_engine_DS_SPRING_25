from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import platform



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
        urls = self.lineEdit.text()
        if urls:
            url_list = [url.strip() for url in urls.split(',')]
            url_list_str = ','.join(url_list)

            system_platform = platform.system()

            if system_platform == "Linux":
                subprocess.Popen(["gnome-terminal", "--", "mpiexec", "-n", "6", "python", "-m", "Master.master_node", url_list_str])

            elif system_platform == "Windows":
                subprocess.Popen(["cmd.exe", "/k", f"mpiexec -n 6 python -m Master.master_node {url_list_str}"])

            elif system_platform == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Terminal.app", f"mpiexec -n 6 python -m Master.master_node {url_list_str}"])

            else:
                QtWidgets.QMessageBox.warning(None, "Unsupported OS", f"Your OS ({system_platform}) is not supported for this operation.")
        
        else:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please enter at least one URL to start the process.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
