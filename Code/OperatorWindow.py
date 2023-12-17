from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os

# Importing required classes
import AddInstallmentWindow
import ClientFromWindow
import ExistedCustomer
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

####################################### Operator Class ###########################################
class OperatorWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the OperatorWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "opretorWindow.ui", self)
        self.setWindowTitle("Operator Window")
        self.parent = parent
        self.addNewCustomer.clicked.connect(self.on_customerSelect) 
        self.addInstallment.clicked.connect(self.on_addInstallment)
        self.signOut_btn.clicked.connect(self.on_signout_btn)

    def on_signout_btn(self):
        """
        Close the current OperatorWindow and open the LoginWindow when the sign-out button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = LoginWindow.LoginWindow()
        self.new.show()
        self.close()

    def on_customerSelect(self):
        """
        Determine whether to add a new customer or select an existing customer based on the selected option.

        Parameters:
        - None

        Returns:
        - None
        """
        if self.comboCustomer.currentText() == 'Existing Customer':
            self.existingCustomer()
        elif self.comboCustomer.currentText() == 'New Customer':
            self.newCustomer()

    def newCustomer(self):
        """
        Open the ClientFromWindow for adding a new customer.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ClientFromWindow.ClientFromWindow()
        self.new.show()
        self.close()

    def existingCustomer(self):
        """
        Open the ExistedCustomer window for selecting an existing customer.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ExistedCustomer.ExistedCustomer()
        self.new.show()
        self.close()

    def on_addInstallment(self):
        """
        Open the AddInstallmentWindow for adding a new installment.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = AddInstallmentWindow.AddInstallmentWindow()
        self.new.show()
        self.close()
