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

# Initialize a variable to store the manager's name
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
        # Load the UI file for the main window
        uic.loadUi(absolutePath + "mainwindow.ui", self)
        self.setWindowTitle("Installment management system")

        # Connect the button click signal to the login function
        self.pushButton2.clicked.connect(self.loginfunction)

    def loginfunction(self):
        """
        Function to handle the login button click event.

        Returns:
        - None
        """
        # Create an instance of the LoginWindow class
        self.new = LoginWindow.LoginWindow()
        # Show the login window
        self.new.show()
        # Close the main window
        self.close()

# Entry point for the application
if __name__ == "__main__":
    # Create a PyQt application instance
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Start the application event loop
    app.exec_()
