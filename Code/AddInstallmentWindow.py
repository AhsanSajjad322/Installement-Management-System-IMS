# Import necessary modules
from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

# Importing required classes
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

####################################### Installment Class ###########################################

class AddInstallmentWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the AddInstallmentWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "addInstallment.ui", self)
        self.setWindowTitle("Add Installment")
        self.parent = parent
        self.cus_Info.hide()
        self.tabWidget.tabBar().setVisible(False)
        self.Home5.clicked.connect(self.on_home_btn)
        self.Home6.clicked.connect(self.on_home_btn)
        self.search_btn1.clicked.connect(self.showInfo)
        self.addInstallementButton.clicked.connect(self.showTab1)
        self.pushButton_3.clicked.connect(self.on_add_Installement)
        self.newPrev.clicked.connect(self.showTab0)

    def showTab1(self):
        """
        Switch to tab 1 and hide the 'Add Installment' button.

        Parameters:
        - None

        Returns:
        - None
        """
        self.addInstallementButton.hide()
        self.tabWidget.setCurrentIndex(1)

    def showTab0(self):
        """
        Switch to tab 0 and show the 'Add Installment' button.

        Parameters:
        - None

        Returns:
        - None
        """
        self.addInstallementButton.show()
        self.tabWidget.setCurrentIndex(0)

    def showTable(self, data):
        """
        Display data in the table widget.

        Parameters:
        - data: List of tuples containing data to be displayed in the table.

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

    def showInfo(self):
        """
        Display customer information based on the provided Account No.

        Parameters:
        - None

        Returns:
        - None
        """
        self.cus_Info.show()
        AccountNo = self.lineEdit.text()

        try:
            # Updating Fields
            query = f"SELECT CONCAT(Customer.FirstName,' ', Customer.LastName), Account.ProductName, Payment.TotalAmount, Balance.AmountRemaining, InstallementRecord.RemainingInstallements, InstallementRecord.TotalInstallements, Payment.MonthlyPayable FROM Account JOIN Customer USING (C_ID) JOIN Payment USING(AccountNo) JOIN Product USING(ProductName) JOIN Balance USING(AccountNo) JOIN InstallementRecord USING (AccountNo) WHERE AccountNo = {AccountNo}"
            
            mycursor.execute(query)
            data = mycursor.fetchall()

            TotalInstallements = int(data[0][5])
            paid = (int(data[0][5])) - (int(data[0][4]))
            self.label_10.setText(data[0][0])
            self.label_13.setText(data[0][1])
            self.label_12.setText(str(data[0][2]))
            self.label_14.setText(str(data[0][3]))
            self.label_17.setText(str(data[0][4]))
            self.label_46.setText(str(data[0][6]))
            self.label_15.setText(str(TotalInstallements))
            self.label_18.setText(str(paid))

            query = f"SELECT InstallementNo, ReceivedInstallementDate, InstallementAmount FROM Installement WHERE AccountNo = {AccountNo} "
            mycursor.execute(query)
            data = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            self.showTable(data)
        except Exception as e:
            print(e)

    def on_add_Installement(self):
        """
        Process the addition of a new installment.

        Parameters:
        - None

        Returns:
        - None
        """
        AccountNo = self.lineEdit_2.text()
        ReceivedInstallementDate = self.lineEdit_3.text()
        ReceivedAmount = self.lineEdit_4.text()

        try:
            # Decreasing Remaining Installements by 1
            mycursor.execute(f"UPDATE InstallementRecord SET RemainingInstallements = RemainingInstallements - 1 WHERE AccountNo = {AccountNo}")
            mydb.commit()

            # Fetching Remaining Installements From InstallementRecord
            query = f"SELECT RemainingInstallements FROM InstallementRecord WHERE AccountNo = {AccountNo}"
            mycursor.execute(query)
            data = mycursor.fetchall()
            remNoOfInst = data[0][0]
            status = "Dead"
            if remNoOfInst == 0:
                # Updating Account Status in Accounts table
                mycursor.execute(f"UPDATE Account SET Status ={status} WHERE AccountNo = {AccountNo}")
                mydb.commit()

            # Fetching No Of Installement No From InstallementRecord Table
            query = f"SELECT TotalInstallements, RemainingInstallements FROM InstallementRecord WHERE AccountNo = {AccountNo}"
            mycursor.execute(query)
            data = mycursor.fetchall()
            InstallementNo = data[0][0] - data[0][1]

            # Adding Data to Installements Table
            mycursor.execute("INSERT INTO Installement(AccountNo, InstallementNo, InstallementAmount, ReceivedInstallementDate) VALUES (%s, %s, %s, %s)",
                             (AccountNo, InstallementNo, ReceivedAmount, ReceivedInstallementDate))
            mydb.commit()

            # Updating Data to Balance Table
            mycursor.execute(f"UPDATE Balance SET AmountRemaining = AmountRemaining - {ReceivedAmount}, AmountPaid = AmountPaid + {ReceivedAmount} WHERE AccountNo = {AccountNo}")
            mydb.commit()

        except Exception as e:
            print(e)

        self.new = OperatorWindow.OperatorWindow()
        self.new.show()
        self.close()

    def on_home_btn(self):
        """
        Navigate to the home screen.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = OperatorWindow.OperatorWindow()
        self.new.show()
        self.close()
