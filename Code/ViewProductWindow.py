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

####################################### Product Class ###########################################
class ViewProductWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        Constructor for the ViewProductWindow class.

        Parameters:
        - parent: Parent widget (default is None).
        """
        super().__init__()
        uic.loadUi(absolutePath + "AddProduct.ui", self)
        self.setWindowTitle("Product Window")
        self.parent = parent
        self.prev_btn.clicked.connect(self.on_prev)
        self.addNew_btn.clicked.connect(self.showTab1)
        self.pushButton_3.clicked.connect(self.showTab0)
        self.pushButton_2.clicked.connect(self.on_save)
        self.label_10.hide()

        self.showProduct()
    
    def on_prev(self):
        """
        Close the current ViewProductWindow and open the ManagerWindow when the previous button is clicked.

        Parameters:
        - None

        Returns:
        - None
        """
        self.new = ManagerWindow.ManagerWindow()
        self.new.show()
        self.close()

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

    def on_save(self):
        """
        Save the product details entered by the user and update the product table in the database.

        Parameters:
        - None

        Returns:
        - None
        """
        pName = self.lineEdit.text()
        category = self.lineEdit_2.text()
        price = self.lineEdit_3.text()
        try:
            mycursor.execute('''
            INSERT INTO product(ProductName, Category, Price) VALUES(%s, %s, %s)
            ''', (pName, category, price))
            mydb.commit()
            print("Product added")
        except Exception as e:
            print("Error:", e)
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")
        self.lineEdit_3.setText("")
        self.label_10.show()

    def getTotalNoOfProducts(self):
        """
        Retrieve the total number of products from the database.

        Parameters:
        - None

        Returns:
        - totalNoOfProducts (int): The total number of products.
        """
        mycursor.execute(''' SELECT COUNT(*) FROM product''')
        totalNoOfProducts = mycursor.fetchall()[0][0]
        return totalNoOfProducts

    def getAllProducts(self):
        """
        Retrieve information about all products from the database.

        Parameters:
        - None

        Returns:
        - products (list): A list containing tuples representing product details.
        """
        mycursor.execute(''' SELECT * FROM product''')
        products = mycursor.fetchall()
        return products


    def showProduct(self):
        """
        Display the total number of products and the product details in the table.

        Parameters:
        - None

        Returns:
        - None
        """
        total = 0
        try:
            total = self.getTotalNoOfProducts()
        except Exception as e:
            print("Error:", e)
        self.label_2.setText(str(total))

        data = []
        try:
            data = self.getAllProducts()
        except Exception as e:
            print("Error:", e)
        self.showTable(data)

    def showTable(self, data):
        """
        Display product information in the table.

        Parameters:
        - data: List of tuples containing product information.

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
