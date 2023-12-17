from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os
from datetime import date

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

####################################### Record Class ###########################################
class ViewRecordWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ViewRecordWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "Records.ui", self)
        self.setWindowTitle("Record Window")
        self.parent = parent
        self.prev_btn.clicked.connect(self.on_prev)
        self.pushButton.clicked.connect(self.on_app)
        self.show_record()   
    
    def month(self):
        """
        Get the selected month.

        Parameters:
        - None

        Returns:
        - str: Selected month as a string.
        """
        m = self.comboBox_3.currentText()
        today = date.today()
        
        if m == "Current":
            return today.month
        else:
            p = {
                "Jan": "01","Feb": "02","Mar": "03","Apr": "04","May": "05","Jun": "06","Jul": "07",
                "Aug": "08","Sep": "09","Oct": "10","Nov": "11","Dec": "12"
            }
            return p.get(m)

    def getNoOfAccountsCreatedInMonth(self, month):
        """
        Retrieves the number of new accounts created in a specified month.

        Parameters:
        - month (str): The month for which the count is to be obtained.

        Returns:
        - int: The number of new accounts created in the specified month.
        """
        query = "SELECT count(*) FROM account WHERE DateOfCreation LIKE '_____{}%'".format(month)
        mycursor.execute(query)
        noOfNewAccounts = mycursor.fetchall()[0][0]
        return noOfNewAccounts
    
    def getNoOfAccountsClearedInMonth(self, month):
        """
        Retrieves the number of accounts marked as 'Dead' (cleared) in a specified month.

        Parameters:
        - month (str): The month for which the count is to be obtained.

        Returns:
        - int: The number of accounts marked as 'Dead' in the specified month.
        """
        query = "SELECT count(*) FROM account WHERE DateOfCreation LIKE '_____{}%' AND Status ='Dead'".format(month)
        mycursor.execute(query)
        noOfAccountsCleared = mycursor.fetchall()[0][0]
        return noOfAccountsCleared
    
    def getNoOfAccountsRecoveredInMonth(self, month):
        """
        Retrieves the number of accounts for which an installment was received in a specified month.

        Parameters:
        - month (str): The month for which the count is to be obtained.

        Returns:
        - int: The number of accounts for which an installment was received in the specified month.
    """
        query = "SELECT COUNT(*) FROM installement WHERE ReceivedInstallementDate LIKE '_____{}%'".format(month)
        mycursor.execute(query)
        noOfAccountsRecovered = mycursor.fetchall()[0][0]
        return noOfAccountsRecovered
    
    def getNoOfAccountsNotRecoveredInMonth(self, month):
        """
        Retrieves the number of accounts for which no installment was received in a specified month.

        Parameters:
        - month (str): The month for which the count is to be obtained.

        Returns:
        - int: The number of accounts for which no installment was received in the specified month.
        """
        query = "SELECT COUNT(*) FROM installement WHERE ReceivedInstallementDate NOT LIKE '_____{}%'".format(month)
        mycursor.execute(query)
        noOfAccountNotRecovered = mycursor.fetchall()[0][0]
        return noOfAccountNotRecovered
    
    def getNoOfProductsSoldInMonth(self, month):
        """
        Retrieves the number of products sold in a specified month.

        Parameters:
        - month (str): The month for which the count is to be obtained.

        Returns:
        - int: The number of products sold in the specified month.
        """
        query = "SELECT COUNT(*) FROM payment WHERE DateOfPurchased LIKE '_____{}%'".format(month)
        mycursor.execute(query)
        noOfProdSold = mycursor.fetchall()[0][0]
        return noOfProdSold

    def show_record(self):
        """
        Display various records in the GUI based on the selected month.

        Parameters:
        - None

        Returns:
        - None
        """
        new_acc = 0
        cleared_acc = 0
        acc_rec = 0
        acc_to_rec = 0
        prod_sell = 0
        mon = self.month()

        new_acc = self.getNoOfAccountsCreatedInMonth(mon)
        cleared_acc = self.getNoOfAccountsClearedInMonth(mon)
        acc_rec = self.getNoOfAccountsRecoveredInMonth(mon)
        acc_to_rec = self.getNoOfAccountsNotRecoveredInMonth(mon)
        prod_sell = self.getNoOfProductsSoldInMonth(mon)

        self.label_4.setText(str(new_acc))
        self.label_8.setText(str(cleared_acc))
        self.label_11.setText(str(acc_rec))
        self.label_23.setText(str(acc_to_rec))
        self.label_6.setText(str(prod_sell))

    def on_prev(self):
        """
        Close the current ViewRecordWindow and open the ManagerWindow when the previous button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ManagerWindow.ManagerWindow()
        self.new.show()
        self.close()
        
    def on_app(self):
        """
        Update and display records when the refresh button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.show_record()
