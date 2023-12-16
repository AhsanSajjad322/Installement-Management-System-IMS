import unittest
import sys
import os

# Add the root project directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AddInstallmentWindow import AddInstallmentWindow
from ClientFromWindow import ClientFromWindow

# Testing AddInstallementWindow File
class TestAddInstallement(unittest.TestCase):
    """
    Test case class for testing the methods of the AddInstallmentWindow class.

    Testing Strategy:
    - Test the getCustomer method with known account details.
    - Test the getInstallementDetails method with known account details.

    Test Cases:
    - testNawazGetCustomer: Test the getCustomer method for a specific account (Nawaz Sharif).
    - testNawazInstallementDetails: Test the getInstallementDetails method for a specific account (Nawaz Sharif).
    - testAbdulGetCustomer: Test the getCustomer method for a specific account (Abdul Basit).
    - testAbdulInstallementDetails: Test the getInstallementDetails method for a specific account (Abdul Basit).
    """
    def setUp(self):
        # Test data for Nawaz Sharif and Abdul Basit
        self.nawazInfo = [('Nawaz Sharif', 'Fan', 14000, 8665, 6, 9, 1445)]
        self.nawazAccountNo = 5
        self.nawazInstallementDetials = [(1, '2022-10-06', 1445), (2, '2022-12-09', 1445), (3, '2023-01-09', 1445)]
        self.abdulInfo = [('Abdul  Basit', 'Air Cooler', 22500, 13664, 8, 12, 1709)]
        self.abdulAccountNo = 3
        self.abdulInstallementDetials = [(1, '2022-08-09', 1709), (2, '2022-09-09', 1709), (3, '2022-10-09', 1709), (4, '2022-12-11', 1709)]

    def testNawazGetCustomer(self):
        customerDetials = AddInstallmentWindow.getCustomer(self, self.nawazAccountNo)
        self.assertEqual(customerDetials, self.nawazInfo )

    def testNawazInstallementDetails(self):
        installementDetails = AddInstallmentWindow.getInstallementDetials(self, self.nawazAccountNo)
        self.assertEqual(installementDetails, self.nawazInstallementDetials )
    
    def testAbdulGetCustomer(self):
        customerDetials = AddInstallmentWindow.getCustomer(self, self.abdulAccountNo)
        self.assertEqual(customerDetials, self.abdulInfo )

    def testAbdulInstallementDetails(self):
        installementDetails = AddInstallmentWindow.getInstallementDetials(self, self.abdulAccountNo)
        self.assertEqual(installementDetails, self.abdulInstallementDetials )

# Testing ClientFormWindow File
class TestClientForm(unittest.TestCase):
    """
    Test case class for testing the methods of the ClientFormWindow class.

    Testing Strategy:
    - Test the getCustomerByCNIC method with known CNIC.

    Test Cases:
    - testCustomerDetails: Test the getCustomerByCNIC method for a specific CNIC.
    """
    def setUp(self):
        # Test data for the customer with CNIC "123456789"
        self.customerDetials = [(104, 'Ali', 'Akbar', 'Attar Hostel', '123456789', '03239008674', '03485998674', 50000, 'Akbar', 'Single', 'M', '20-09-2000', 'NUST')]
        self.customerCNIC = "123456789"

    def testCustomerDetials(self):
        customerDetials = ClientFromWindow.getCustomerByCNIC(self, self.customerCNIC)
        self.assertEqual(customerDetials, self.customerDetials)

if __name__ == "__main__":
    unittest.main()
