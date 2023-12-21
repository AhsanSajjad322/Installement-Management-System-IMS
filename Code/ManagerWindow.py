from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os

# Importing required classes
import LoginWindow
import NewEmployeeWindow
import ViewCustomerWindow
import ViewEmployeeWindow
import ViewProductWindow
import ViewRecordWindow

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

####################################### Manager Class ###########################################
class ManagerWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ManagerWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "managerWindow.ui", self)
        self.setWindowTitle("Manager Window")
        self.parent = parent
        self.add_employee_btn.clicked.connect(self.on_addEmployee)
        self.view_employee_btn.clicked.connect(self.on_viewEmployee)
        self.view_customer_btn.clicked.connect(self.on_viewCustomer)
        self.view_record_btn.clicked.connect(self.on_viewRecord)
        self.view_product_btn.clicked.connect(self.on_viewProduct)
        self.signOut_btn.clicked.connect(self.on_signout_btn)

    def on_addEmployee(self):
        """
        Open the window to add a new employee.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = NewEmployeeWindow.NewEmployeeWindow()
        self.new.show()
        self.close()

    def on_viewEmployee(self):
        """
        Open the window to view employee information.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ViewEmployeeWindow.ViewEmployeeWindow()
        self.new.show()
        self.close()

    def on_viewCustomer(self):
        """
        Open the window to view customer information.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ViewCustomerWindow.ViewCustomerWindow()
        self.new.show()
        self.close()

    def on_viewRecord(self):
        """
        Open the window to view installment records.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ViewRecordWindow.ViewRecordWindow()
        self.new.show()
        self.close()

    def on_viewProduct(self):
        """
        Open the window to view product information.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ViewProductWindow.ViewProductWindow()
        self.new.show()
        self.close()

    def on_signout_btn(self):
        """
        Open the login window when the sign-out button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = LoginWindow.LoginWindow()
        self.new.show()
        self.close()
