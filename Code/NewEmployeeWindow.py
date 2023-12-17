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

manager_name = ""

class NewEmployeeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the NewEmployeeWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "addEmployee.ui", self)
        self.setWindowTitle("Add Employee")
        self.parent = parent
        self.prev_btn.clicked.connect(self.on_prev)
        self.add_btn.clicked.connect(self.on_add)

    def mId(self):
        """
        Retrieve the Manager ID associated with the logged-in manager.

        Parameters:
        - None

        Returns:
        - int: Manager ID
        """
        mId = 0
        try:
            query = "SELECT M_ID FROM manager WHERE Name = '{}'".format(manager_name)
            mycursor.execute(query)
            mId = mycursor.fetchall()[0][0]
        except Exception as e:
            print(e)
        print(mId)
        return mId

    def on_prev(self):
        """
        Navigate back to the ManagerWindow when the previous button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ManagerWindow.ManagerWindow()
        self.new.show()
        self.close()

    def on_add(self):
        """
        Add a new employee to the database when the add button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        fn = self.first_name.text()
        ln = self.last_name.text()
        cin = self.cnic.text()
        Fn = self.father_name.text()
        dob = self.dob.text()
        gen = self.comboBox.currentText()
        phone = self.phone.text()
        desig = self.comboBox_2.currentText()
        mart = self.comboBox_3.currentText()
        addr = self.address.text()
        work = self.work_hours.text()
        salary = self.salary.text()
        mid = self.mId()
        print(fn, ln, cin, Fn, dob, gen, phone, desig, mart, addr, work, salary, mid)
        try:
            mycursor.execute('''
            INSERT INTO employee(M_ID,FirstName,LastName,CNIC,Salary,WorkHours,Address,DOB,Gender,FatherName,
            Designation,PhoneNo,Martial_status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (mid, fn, ln, cin, salary, work, addr, dob, gen, Fn, desig, phone, mart))
            mydb.commit()
        except Exception as e:
            print(e)
