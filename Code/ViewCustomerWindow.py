from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os

# Importing required classes
import ManagerWindow

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

####################################### View Customer Class ###########################################
class ViewCustomerWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ViewCustomerWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "viewCustomerWindow.ui", self)
        self.setWindowTitle("Customers Window")
        self.parent = parent
        self.prev_btn.clicked.connect(self.on_prev)
        self.pushButton.clicked.connect(self.on_search)
        self.app_btn.clicked.connect(self.on_app_btn)
        self.showInfo()

    def on_prev(self):
        """
        Close the current ViewCustomerWindow and open the ManagerWindow when the previous button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ManagerWindow.ManagerWindow()
        self.new.show()
        self.close()

    def on_search(self):
        """
        Search for customer information based on the provided account number and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        acc = self.lineEdit.text()
        arg = [acc]
        data = []
        try:
            mycursor.callproc("show_customer_info", arg)
            for result in mycursor.stored_results():
                data = result.fetchall()
        except Exception as e:
            print(e)
        self.lineEdit.setText("")
        self.tableWidget.setRowCount(0)
        self.showTable(data)

    def getTotalNoOfAccounts(self):
        """
        Retrieve the total number of accounts from the database.

        Parameters:
        - None

        Returns:
        - total (int): The total number of accounts.
        """
        q = "SELECT COUNT(*) FROM account"
        mycursor.execute(q)
        total = mycursor.fetchall()[0][0]
        return total

    def getNoOfActiveAccounts(self):
        """
        Retrieve the number of active accounts from the database.

        Parameters:
        - None

        Returns:
        - noOfActiveAccounts (int): The number of active accounts.
        """
        q = "SELECT COUNT(*) FROM account WHERE status = 'Active'"
        mycursor.execute(q)
        noOfActiveAccounts = mycursor.fetchall()[0][0]
        return noOfActiveAccounts

    def getAllAccounts(self):
        """
        Retrieve information about all accounts from the database.

        Parameters:
        - None

        Returns:
        - allAccounts (list): A list containing tuples representing account details.
        """
        q = "SELECT AccountNo,C_ID, concat(FirstName,' ',LastName),ProductName,MobileNo,MonthlyIncome,gender,status,PlaceOfWork FROM account JOIN customer USING(C_ID)"
        mycursor.execute(q)
        allAccounts = mycursor.fetchall()
        return allAccounts

    def getCustomersOnFilter(self, filt):
        """
        Retrieve customer information based on a specified filter from the database.

        Parameters:
        - filt (str): The filter to apply (e.g., 'Active').

        Returns:
        - data (list): A list containing tuples representing customer details based on the filter.
        """
        q = "SELECT AccountNo,C_ID, concat(FirstName,' ',LastName),ProductName,MobileNo,MonthlyIncome,gender,status,PlaceOfWork FROM account JOIN customer USING(C_ID) WHERE Status = '{}'".format(filt)
        mycursor.execute(q)
        data = mycursor.fetchall()
        return data


    def showInfo(self):
        """
        Display general information about the total, active, and inactive (dead) customers.

        Parameters:
        - None

        Returns:
        - None
        """
        total = 0
        active = 0
        data = []
        try:
            total = self.getTotalNoOfAccounts()
        except Exception as e:
            print(e)
        try:
            active = self.getNoOfActiveAccounts()
        except Exception as e:
            print(e)
        dead = total - active
        self.label_6.setText(str(total))
        self.label_7.setText(str(active))
        self.label_8.setText(str(dead))
        try:
            data = self.getAllAccounts()
        except Exception as e:
            print(e)
        self.showTable(data)

    def on_app_btn(self):
        """
        Filter customer information based on the selected status and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        filt = self.comboBox.currentText()
        data = []
        try:
            data = self.getCustomersOnFilter(filt)
        except Exception as e:
            print(e)
        self.tableWidget.setRowCount(0)
        self.showTable(data)

    def showTable(self, data):
        """
        Display customer information in the table.

        Parameters:
        - data: List of tuples containing customer information.

        Returns:
        - None
        """
        if data:
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
            
            self.tableWidget.verticalHeader().setVisible(False)
