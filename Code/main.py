# Import necessary modules
import sys
import os
from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Import user-defined classes
import LoginWindow

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="InstallementManagementSystem"
)
mycursor = mydb.cursor()

# Get the absolute path for UI files
path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//UI//"
manager_name = ""

# Define the main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        """
        Constructor for the MainWindow class.

        Parameters:
        - args: Variable-length argument list.
        - kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        uic.loadUi(absolutePath + "mainwindow.ui", self)
        self.setWindowTitle("Installment management system")

        self.pushButton2.clicked.connect(self.loginfunction)

    def loginfunction(self):
        """
        Function to handle the login button click event.

        Returns:
        - None
        """

        self.new = LoginWindow.LoginWindow()
        self.new.show()
        self.close()

# Entry point for the application
if __name__ == "__main__":
  
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()


    app.exec_()
