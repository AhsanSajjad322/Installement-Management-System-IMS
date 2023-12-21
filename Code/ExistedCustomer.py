# Import necessary modules
from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os
import math

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

####################################### Existing Customer ###########################################

class ExistedCustomer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ExistedCustomer class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "ExistedCustomer.ui", self)
        self.setWindowTitle("Existing Customer")
        self.parent = parent
        self.tabWidget.tabBar().setVisible(False)
        self.BuyNewProduct.clicked.connect(self.showTab1)
        self.search.clicked.connect(self.showInfo)
        self.newNext1.clicked.connect(self.showTab2)
        self.newPrev1.clicked.connect(self.showTab0)
        self.newPrev2.clicked.connect(self.showTab1)
        self.newHome1.clicked.connect(self.on_home_btn)
        self.newHome2.clicked.connect(self.on_home_btn)
        self.newHome3.clicked.connect(self.on_home_btn)
        self.Home5.clicked.connect(self.on_home_btn)
        self.newSaveButton.clicked.connect(self.on_safe_btn)
        self.Done.clicked.connect(self.on_home_btn)
    
    def getDetailedCustomerByCNIC(self, CNIC):
        """
        Retrieve detailed customer information based on CNIC.

        Parameters:
        - CNIC: Customer CNIC.

        Returns:
        - List of tuples containing detailed customer information.
        """
        query = f"SELECT CONCAT(Customer.FirstName,' ',Customer.LastName), Customer.PhoneNo, Customer.MonthlyIncome,Customer.FatherName,Customer.MartialStatus, Account.ProductName, Product.Price, Account.Status, CONCAT(Guarantor.FirstName,' ' ,Guarantor.LastName) FROM Customer JOIN Account USING(C_ID) JOIN Product USING(ProductName) JOIN GuarantiedBy USING(C_ID) JOIN Guarantor USING(G_CNIC) WHERE Customer.CNIC = '{CNIC}'"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data

    def getCustomerByCNIC(self, CNIC):
        """
        Retrieve customer information based on CNIC.

        Parameters:
        - CNIC: Customer CNIC.

        Returns:
        - List of tuples containing customer information.
        """
        query = f"SELECT * FROM Customer WHERE CNIC = '{CNIC}'"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data

    def showInfo(self):
        """
        Display customer information based on the provided CNIC.

        Parameters:
        - None

        Returns:
        - None
        """
        CNIC = self.lineEdit.text()
        try:
            data = self.getDetailedCustomerByCNIC(CNIC)
            
        except:
            print("Error")
        self.showTable(data)

    def showTab1(self):
       """
       Switch to tab 1.

       Parameters:
       - None

       Returns:
       - None
       """
       self.tabWidget.setCurrentIndex(1)

    def showTab0(self):
       """
       Switch to tab 0 and show customer information.

       Parameters:
       - None

       Returns:
       - None
       """
       self.ExistedInfo.show()
       self.tabWidget.setCurrentIndex(0)

    def showTab2(self):
       """
       Switch to tab 2.

       Parameters:
       - None

       Returns:
       - None
       """
       self.tabWidget.setCurrentIndex(2)

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

    def on_safe_btn(self):
        """
        Process the form data and display customer details.

        Parameters:
        - None

        Returns:
        - None
        """
        ## Product Information
        PName = self.lineEdit_26.text()
        PDate = self.lineEdit_34.text()
        NetAmount = self.lineEdit_39.text()
        Advance = self.lineEdit_37.text()
        NoOfMonths = int(self.comboBox.currentText())

        ## Calculating Required Figures
        if(NoOfMonths==3):
            AddedAmount = (int(NetAmount)*20)/100
        elif(NoOfMonths==6):
            AddedAmount = (int(NetAmount)*30)/100
        elif(NoOfMonths==9):
            AddedAmount = (int(NetAmount)*40)/100
        elif(NoOfMonths==12):
            AddedAmount = (int(NetAmount)*50)/100

        TotalAmount = int(NetAmount) + math.ceil(AddedAmount)
        Remaining = TotalAmount - int(Advance)
        InstallementPerMonth = math.ceil(Remaining/int(NoOfMonths))
        
        print("Net Amount :",NetAmount)
        print("No Of Months :",NoOfMonths)
        print("Total Amount :",TotalAmount)
        print("Advance :",Advance)
        print("Installement/Month :",InstallementPerMonth)
        print("Remaining :",Remaining)
        
        ## Customer Information
        CNIC = self.lineEdit.text()
        
        ## Account Information
        E_ID = self.lineEdit_24.text()
        CreationDate = PDate
        ExpectedDuration = self.lineEdit_40.text()
        status = "Active"
        InstallementDate = self.lineEdit_68.text()
        
        try:
            ## Fetching Customer ID FROM Database
            data = self.getCustomerByCNIC(CNIC)
            C_ID = data[0][0]
            print("Customer ID: ",C_ID)

            ## Inserting Data In Account Table
            mycursor.execute('''INSERT INTO Account(E_ID,C_ID,ProductName,DateOfCreation,ExpectedDuration,Status) VALUES(%s,%s,%s,%s,%s,%s)
            ''',(E_ID,C_ID,PName,CreationDate,ExpectedDuration,status))
            mydb.commit()
            print("Accounts Added")

            ## Fetching AccountNo From Database
            query = f"SELECT * FROM Account WHERE C_ID = {C_ID} AND DateOfCreation = '{CreationDate}'"
            mycursor.execute(query)
            data = mycursor.fetchall()
            AccountNo = data[0][0]
            print("Account No Fetched : ",AccountNo)

            ## Inserting Data In Payment Table
            mycursor.execute('''INSERT INTO Payment(AccountNo,DateOfPurchased,NetAmount,TotalAmount,Advance,RemainingBalance,MonthlyPayable) VALUES (%s,%s,%s,%s,%s,%s,%s)
            ''',(AccountNo,CreationDate,NetAmount,TotalAmount,Advance,Remaining,InstallementPerMonth))
            mydb.commit()
            print("Payment Added")

            ## Inserting Data In Balance Table
            mycursor.execute('''INSERT INTO Balance(AccountNo,DateofInstallement,AmountRemaining,AmountPaid) VALUES(%s,%s,%s,%s)
            ''',(AccountNo,InstallementDate,Remaining,Advance))
            mydb.commit()
            print("Balance Added")

            ## Inserting Data In InstallementRecord Table
            mycursor.execute('''INSERT INTO InstallementRecord(AccountNo,RemainingInstallements,TotalInstallements) VALUES (%s,%s,%s)
            ''',(AccountNo,NoOfMonths,NoOfMonths))
            mydb.commit()
            print("Installement Record Added")

            ## Fetching Customer ID from Database
            
            data = self.getCustomerByCNIC(CNIC)
            newC_ID = data[0][0]
            ## Fetching AccountNo From Database
            query = f"SELECT * FROM Account WHERE C_ID = {newC_ID} AND DateOfCreation = '{CreationDate}'"
            mycursor.execute(query)
            data = mycursor.fetchall()
            newAccountNo = data[0][0]
            print("Account No Fetched : ",newAccountNo)

            query = f"SELECT Account.AccountNo, CONCAT(Customer.FirstName,' ',Customer.LastName), Payment.MonthlyPayable, Balance.DateofInstallement FROM Account JOIN Customer USING(C_ID) JOIN payment USING(AccountNo) JOIN Balance USING(AccountNo) WHERE AccountNo = {newAccountNo}"
            mycursor.execute(query)
            data = mycursor.fetchall()
            print(data)
            self.label_16.setText(str(data[0][0]))
            self.label_17.setText(str(data[0][1]))
            self.label_30.setText(str(data[0][2]))
            self.label_32.setText(str(data[0][3]))
            self.tabWidget.setCurrentIndex(3)
        except:
            print("error")


    def showTable(self, data):
        """
        Display data in the table widget.

        Parameters:
        - data: List of tuples containing data to be displayed in the table.

        Returns:
        - None
        """
        if data:
            self.ExistedInfo.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ExistedInfo.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ExistedInfo.rowCount()
                self.ExistedInfo.insertRow(row_position)
