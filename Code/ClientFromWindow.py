from PyQt5 import QtWidgets, uic
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os
import math

# Importing required classes
import OperatorWindow

mydb = mysql.connector.connect(
  host="localhost",   # Specify the Host
  user="root",        # Spwcify The user of the Database
  password="123456",  # Specify the password for that user
  database="InstallementManagementSystem"   # Name of Database Created in MySQl Workbench
)
mycursor = mydb.cursor()


path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//UI//"

####################################### Costomer Class ###########################################

class ClientFromWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "clientForm.ui", self)
        self.setWindowTitle("Customer From")
        self.parent = parent
        self.tabWidget.tabBar().setVisible(False)
        self.Next1.clicked.connect(self.showTab1)
        self.Next2.clicked.connect(self.showTab2)
        self.Next3.clicked.connect(self.showTab3)
        self.Prev1.clicked.connect(self.showTab0)
        self.Prev2.clicked.connect(self.showTab1)
        self.Prev3.clicked.connect(self.showTab2)
        self.Home1.clicked.connect(self.on_home_btn)
        self.Home2.clicked.connect(self.on_home_btn)
        self.Home3.clicked.connect(self.on_home_btn)
        self.Home4.clicked.connect(self.on_home_btn)
        self.Home5.clicked.connect(self.on_home_btn)
        self.saveButton.clicked.connect(self.on_save_btn)
        self.Done.clicked.connect(self.on_home_btn)
        
        
    def showTab1(self):
       self.tabWidget.setCurrentIndex(1)
    def showTab0(self):
       self.tabWidget.setCurrentIndex(0)
    def showTab2(self):
       self.tabWidget.setCurrentIndex(2)
    def showTab3(self):
        self.tabWidget.setCurrentIndex(3)
    def showTab4(self):
        self.tabWidget.setCurrentIndex(4)   

    def on_home_btn(self):
        self.new = OperatorWindow.OperatorWindow()
        self.new.show()
        self.close()
    def on_save_btn(self):
        ## Customer Information
        FirstName = self.lineEdit.text()
        LastName = self.lineEdit_2.text()
        CNIC =  self.lineEdit_3.text()
        FatherName = self.lineEdit_4.text()
        DOB = self.lineEdit_5.text()
        Gender = self.lineEdit_6.text()
        PhoneNo = self.lineEdit_7.text()
        MobileNo =  self.lineEdit_8.text()
        MartialStatus = self.lineEdit_9.text()
        Address = self.lineEdit_10.text()
        WorkPlace = self.lineEdit_11.text()
        Income = self.lineEdit_12.text()
        print("FirstName :"+FirstName)

        ## Guarantor Information
        GFirstName = self.lineEdit_23.text()
        GLastName = self.lineEdit_16.text()
        GCNIC = self.lineEdit_17.text()
        GAddress = self.lineEdit_18.text()
        GPhone = self.lineEdit_19.text()
        GMobile = self.lineEdit_20.text()
        GRelation = self.lineEdit_21.text()
        GWorkPlace = self.lineEdit_22.text()

        ## Product Information
        PName = self.lineEdit_25.text()
        PDate = self.lineEdit_31.text()
        NetAmount = self.lineEdit_27.text()
        Advance = self.lineEdit_28.text()
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

        ## Fields To be Updated
        
        TotalAmount = int(NetAmount) + math.ceil(AddedAmount)
        Remaining = TotalAmount - int(Advance)
        InstallementPerMonth = math.ceil(Remaining/int(NoOfMonths))
        print("Net Amount :",NetAmount)
        print("No Of Months :",NoOfMonths)
        print("Total Amount :",TotalAmount)
        print("Advance :",Advance)
        print("Installement/Month :",InstallementPerMonth)
        print("Remaining :",Remaining)

        ## Account Information
        E_ID = self.lineEdit_15.text()
        CreationDate = PDate
        ExpectedDuration = self.lineEdit_33.text()
        status = "Active"
        InstallementDate = self.lineEdit_67.text()

        try:
            ## Inserting Data In Customer Table
            print(FirstName,LastName,Address,CNIC,PhoneNo,MobileNo,Income,FatherName,MartialStatus,Gender,DOB,WorkPlace)
            mycursor.execute('''
            INSERT INTO Customer(FirstName,LastName,Address,CNIC,PhoneNo,MobileNo,MonthlyIncome,FatherName,MartialStatus,Gender,DOB,PlaceOfWork) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(FirstName,LastName,Address,CNIC,PhoneNo,MobileNo,Income,FatherName,MartialStatus,Gender,DOB,WorkPlace))
            mydb.commit()

            print("Customer Added")

            ## Inserting Data In Guarantor Table
            mycursor.execute('''
            INSERT INTO Guarantor(G_CNIC,FirstName,LastName,Address,PhoneNo,MobileNo,Relation,PlaceOfWork) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(GCNIC,GFirstName,GLastName,GAddress,GPhone,GMobile,GRelation,GWorkPlace))
            mydb.commit()
            print("Guarantor Added")

            ## Fetching Customer ID from Database
            query = f"SELECT * FROM Customer WHERE CNIC = '{CNIC}'"
            mycursor.execute(query)
            data = mycursor.fetchall()
            print(data)
            C_ID = data[0][0]
            print("C_ID Fetched ",C_ID)

            ## Inserting Data In GuarantiedBy Table
            mycursor.execute('''INSERT INTO GuarantiedBy(C_ID,G_CNIC) VALUES(%s,%s)
            ''',(C_ID,GCNIC))
            mydb.commit()
            print("Guarantied By Added")

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
            RemainingNoOfInstallements = int(NoOfMonths)
            mycursor.execute('''INSERT INTO Payment(AccountNo,DateOfPurchased,NetAmount,TotalAmount,Advance,RemainingBalance,MonthlyPayable) VALUES (%s,%s,%s,%s,%s,%s,%s)
            ''',(AccountNo,CreationDate,NetAmount,TotalAmount,Advance,Remaining,InstallementPerMonth))
            mydb.commit()
            print("Payment Added")


            ## Inserting Data In Balance Table
            mycursor.execute('''INSERT INTO Balance(AccountNo,DateofInstallement,AmountRemaining,AmountPaid) VALUES(%s,%s,%s,%s)
            ''',(AccountNo,InstallementDate,Remaining,Advance))
            mydb.commit()
            print("Balance Added")

            ## Inserting Data In InstallementsRecord Table
            mycursor.execute('''INSERT INTO InstallementRecord(AccountNo,RemainingInstallements,TotalInstallements) VALUES (%s,%s,%s)
            ''',(AccountNo,RemainingNoOfInstallements,NoOfMonths))
            mydb.commit()
            print("Installement Record Added")
            
            ## Printing Receipt At The End
            ## Fetching Customer ID from Database
            query = f"SELECT * FROM Customer WHERE CNIC = '{CNIC}'"
            mycursor.execute(query)
            data = mycursor.fetchall()
            print(data)
            newC_ID = data[0][0]
            print("C_ID Fetched ",newC_ID)
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
            self.label_27.setText(str(data[0][1]))
            self.label_29.setText(str(data[0][2]))
            self.label_32.setText(str(data[0][3]))
            self.tabWidget.setCurrentIndex(4)

        except Exception as e:
            print(e)
