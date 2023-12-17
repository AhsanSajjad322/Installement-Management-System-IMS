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

####################################### View Employee Class ###########################################
class ViewEmployeeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ViewEmployeeWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "veiwEmployee.ui", self)
        self.setWindowTitle("Employee Window")
        self.parent = parent
        self.prev_btn.clicked.connect(self.on_prev)
        self.tabWidget.tabBar().setVisible(False)
        self.view_btn.clicked.connect(self.showTab1)
        self.b_btn.clicked.connect(self.showTab0)
        self.search_btn.clicked.connect(self.on_search_btn)
        self.apply_btn.clicked.connect(self.filter)
        self.showDetails()
        self.filter()
        ######### Tab 2 #######
        self.search_btn1.clicked.connect(self.showInfo)
        self.frame.hide()
    
    def getTotalNoOfEmployees(self):
        """
        Retrieves the total number of employees.

        Returns:
        - str: The total number of employees as a string.
        """
        mycursor.execute(''' SELECT COUNT(*) FROM employee''')
        totalEmployees = str(mycursor.fetchall()[0][0])
        return totalEmployees
    
    def getTotalNoOfRecoveryCollectors(self):
        """
        Retrieves the total number of employees with the designation 'Recover_Collector'.

        Returns:
        - str: The total number of recovery collectors as a string.
        """
        mycursor.execute("SELECT COUNT(*) FROM employee WHERE Designation = 'Recover_Collector'")
        totalRevoveryCollectors = str(mycursor.fetchall()[0][0])
        return totalRevoveryCollectors
    
    def getTotalNoOfOperators(self):
        """
        Retrieves the total number of employees with the designation 'Operator'.

        Returns:
        - str: The total number of operators as a string.
        """
        mycursor.execute("SELECT COUNT(*) FROM employee WHERE Designation = 'Operator'")
        totalOperators = str(mycursor.fetchall()[0][0])
        return totalOperators
    
    def getAllEmployees(self):
        """
        Retrieves information about all employees.

        Returns:
        - list: A list containing tuples with information about all employees.
        """
        mycursor.execute(''' SELECT E_ID,M_ID, concat(FirstName,' ',LastName),CNIC,FatherName,PhoneNo, Address,DOB,Gender,Designation,WorkHours,Salary,Martial_status FROM employee''')
        allEmployees = mycursor.fetchall()
        return allEmployees

    def getEmployeeByID(self, ID):
        """
        Retrieves information about an employee by their Employee ID.

        Parameters:
        - ID (str): The Employee ID.

        Returns:
        - list: A list containing tuples with information about the specified employee.
        """
        query = "SELECT * FROM employee WHERE E_ID='{}'".format(ID)
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data
    
    def getAllRecoveryCollectorsByDesignation(self, designation):
        """
        Retrieves information about all employees with the designation 'Recover_Collector'.

        Parameters:
        - designation (str): The designation to filter employees.

        Returns:
        - list: A list containing tuples with information about recovery collectors.
        """
        query = "SELECT E_ID,M_ID, concat(FirstName,' ',LastName),CNIC,FatherName,PhoneNo, Address,DOB,Gender,Designation,WorkHours,Salary,Martial_status FROM employee WHERE Designation='{}'".format(designation)
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data
    
    def getAllOperatorsByDesignation(self, designation):
        """
        Retrieves information about all employees with the designation 'Operator'.

        Parameters:
        - designation (str): The designation to filter employees.

        Returns:
        - list: A list containing tuples with information about operators.
        """
        query = "SELECT * FROM employee WHERE Designation='{}'".format(designation)
        mycursor.execute(query)
        data = mycursor.fetchall()
        return data
    
    def showDetails(self):
        """
        Display general details about the total, recovery employees, and operator employees.

        Parameters:
        - None

        Returns:
        - None
        """
        total = ""
        recEmp = ""
        oprEmp = ""
        try:
            total = self.getTotalNoOfEmployees()
        except Exception as e:
            print(e)
        try:
            recEmp = self.getTotalNoOfRecoveryCollectors()
        except Exception as e:
            print(e)
        try:
            oprEmp = self.getTotalNoOfOperators()
        except Exception as e:
            print(e)
        self.label_6.setText(total)
        self.label_7.setText(recEmp)
        self.label_8.setText(oprEmp)

    def showTab1(self):
       """
       Show Tab 1 when the corresponding button is clicked.

       Parameters:
       - None

       Returns:
       - None
       """
       self.tabWidget.setCurrentIndex(1)

    def showTab0(self):
       """
       Show Tab 0 when the corresponding button is clicked.

       Parameters:
       - None

       Returns:
       - None
       """
       self.tabWidget.setCurrentIndex(0)

    def on_prev(self):
        """
        Close the current ViewEmployeeWindow and open the ManagerWindow when the previous button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ManagerWindow.ManagerWindow()
        self.new.show()
        self.close()

    def showEmployee(self):
        """
        Fetch and display all employee details in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        data = []
        try:
            data = self.getAllEmployees()
        except Exception as e:
            print(e)
        self.showTable(data)

    def showTable(self, data):
        """
        Display employee information in the table.

        Parameters:
        - data: List of tuples containing employee information.

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

    def on_search_btn(self):
        """
        Search for employee information based on the provided employee ID and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        emp_id = self.id_entered.text()
        data = []
        try:
            data = self.getEmployeeByID(emp_id)
        except Exception as e:
            print(e)
        self.id_entered.setText("")
        self.tableWidget.setRowCount(0)
        self.showTable(data)

    def recoveryEmp(self):
        """
        Fetch and display recovery employees' details in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        desig = "Recover_Collector"
        data = []
        try:
            data = self.getAllRecoveryCollectorsByDesignation(desig)
        except Exception as e:
            print(e)

        self.tableWidget.setRowCount(0)
        self.showTable(data)

    def operatorEmp(self):
        """
        Fetch and display operator employees' details in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        desig = "Operator"
        data = []
        try:
            data = self.getAllOperatorsByDesignation(desig)
        except Exception as e:
            print(e)

        self.tableWidget.setRowCount(0)
        self.showTable(data)

    def filter(self):
        """
        Filter employee details based on the selected designation and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        filt = self.comboBox.currentText()
        print(filt)
        if filt == "Total":
            self.showEmployee()
        elif filt == "Recovery collectors":
            self.recoveryEmp()
        elif filt == "Operators":
            self.operatorEmp()

    ####################### Tab 2 ##########################
    def showInfo(self):
        """
        Display customer information related to the selected employee in Tab 2.

        Parameters:
        - None

        Returns:
        - None
        """
        self.frame.show()
        global e_ID
        c = 0
        e_ID = self.eId_Entered.text()
        try:
            query = "SELECT COUNT(*) FROM account WHERE E_ID = {}".format(e_ID)
            mycursor.execute(query)
            c = mycursor.fetchall()[0][0]
        except Exception as e:
            print(e)
        self.label_13.setText(str(c))
        arg = [e_ID]
        data = []
        try:
            mycursor.callproc("show_customer_under_emp", arg)
            for result in mycursor.stored_results():
                data = result.fetchall()
        except Exception as e:
           print(e)
        self.eId_Entered.setText("")
        self.tableWidget.setRowCount(0)
        self.showTable2(data)

    def showTable2(self, data):
        """
        Display customer information in the second table.

        Parameters:
        - data: List of tuples containing customer information.

        Returns:
        - None
        """
        if data:
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
            self.tableWidget_2.verticalHeader().setVisible(False)

    ########### Filter data ###############
    def month(self):
        """
        Get the month value corresponding to the selected month in the combo box.

        Parameters:
        - None

        Returns:
        - str: Month value (e.g., "01" for January).
        """
        m = self.comboBox_3.currentText()
        p = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
            "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
        }
        return p.get(m)

    def filt_Rec(self):
        """
        Filter recovered customer information based on the selected month and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        mon = self.month()
        data = []
        try:
            query = "SELECT AccountNo, concat(FirstName,' ',LastName) As Name,ProductName, TotalAmount, AmountPaid, MonthlyPayable,ReceivedInstallementDate,AmountRemaining,RemainingInstallements FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM customer c NATURAL JOIN account a WHERE a.E_ID={})c1 Natural JOIN payment)c2 NATURAL JOIN balance) c3 NATURAL JOIN installementrecord) c4 NATURAL JOIN installement WHERE ReceivedInstallementDate LIKE '_____{}%'".format(e_ID, mon)
            mycursor.execute(query)
            data = mycursor.fetchall()
        except Exception as e:
            print(e)
        self.tableWidget.setRowCount(0)
        self.showTable2(data)

    ####### tobe Rec #########
    def filt_tobe_Rec(self):
        """
        Filter to-be-recovered customer information based on the selected month and display the results in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        mon = self.month()
        data = []
        try:
            query = "SELECT AccountNo, concat(FirstName,' ',LastName) As Name,ProductName, TotalAmount, AmountPaid, MonthlyPayable,ReceivedInstallementDate,AmountRemaining,RemainingInstallements FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM customer c NATURAL JOIN account a WHERE a.E_ID={})c1 Natural JOIN payment)c2 NATURAL JOIN balance) c3 NATURAL JOIN installementrecord) c4 NATURAL JOIN installement WHERE ReceivedInstallementDate NOT LIKE '_____{}%'".format(e_ID, mon)
            mycursor.execute(query)
            data = mycursor.fetchall()
        except Exception as e:
            print(e)
        self.tableWidget_2.setRowCount(0)
        self.showTable2(data)

    def on_app_btn(self):
        """
        Apply filtering based on the selected option (Recovered, TobeRecovered, All) and display the results.

        Parameters:
        - None

        Returns:
        - None
        """
        ch = self.comboBox_2.currentText()
        if ch == "Recovered":
            self.filt_Rec()
        elif ch == "TobeRecovered":
            self.filt_tobe_Rec()
        else:
            self.showInfo()
