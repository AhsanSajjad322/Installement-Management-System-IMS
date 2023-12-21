from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os

# Importing required classes
import ManagerWindow
import OperatorWindow

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

####################################### Login Class ###########################################    
class LoginWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the LoginWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "login.ui", self)
        self.setWindowTitle("Log In")
        self.parent = parent
        self.pushButton.clicked.connect(self.on_loginButton)
        self.label_4.hide()

    def getM_name(self):
        """
        Retrieve and set the manager's name based on the entered username.

        Parameters:
        - None

        Returns:
        - None
        """
        un = self.user_name.text()
        print(un)
        global manager_name
        if un == "yameen12":
            manager_name = "Yameen"
        elif un == "mehran22":
            manager_name = "Mehran"

    def getManagerAccounts(self):
        """
        Retrieve manager accounts from the database.

        Parameters:
        - None

        Returns:
        - managerAccounts (list): A list containing tuples representing manager accounts.
        """
        query = "SELECT * FROM manager_accounts"
        mycursor.execute(query)
        managerAccounts = mycursor.fetchall()
        return managerAccounts

    def getOperatorAccounts(self):
        """
        Retrieve operator accounts from the database.

        Parameters:
        - None

        Returns:
        - operatorAccounts (list): A list containing tuples representing operator accounts.
        """
        query = "SELECT * FROM operator_accounts"
        mycursor.execute(query)
        operatorAccounts = mycursor.fetchall()
        return operatorAccounts

    
    def verifyAccount(self):
        """
        Verify the entered username and password against the database.

        Parameters:
        - None

        Returns:
        - bool: True if the account is verified, False otherwise.
        """
        un = self.user_name.text()
        pas = self.password.text()
        acc = []
        check = False
        if self.managerCheck.isChecked():
            try:
                acc = self.getManagerAccounts()
            except:
                print("error")
            print(un + pas)
            for x in acc:
                if (un == x[0]) & (pas == x[1]):
                    check = True
                    break
        else:
            try:
                acc = self.getOperatorAccounts()
                print(acc)
            except:
                print("error")
            print(un + pas)
            for x in acc:
                if (un == x[0]) & (pas == x[1]):
                    check = True
                    break
        return check

    def on_loginButton(self):
        """
        Handle the login button click event and navigate to the respective window.

        Parameters:
        - None

        Returns:
        - None
        """
        if self.managerCheck.isChecked() and self.verifyAccount():
            self.getM_name()
            self.new = ManagerWindow.ManagerWindow()
            self.new.show()
            self.close()
        elif (not self.managerCheck.isChecked()) and (self.verifyAccount()):
            print(self.verifyAccount())
            self.new = OperatorWindow.OperatorWindow()
            self.new.show()
            self.close()
        else:
            self.label_4.show()
            print("Incorrect Password")
