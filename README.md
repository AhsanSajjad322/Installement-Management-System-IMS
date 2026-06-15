# Installment Management System (IMS)

A desktop-based **Installment Management System** for managing customer purchases, payment plans, employee records, and recovery tracking. The application provides role-based access for **Managers** and **Operators**, with a MySQL backend and a PyQt5 graphical user interface.

---

## Overview

This system allows businesses to sell products on installment plans. Operators register customers, create installment accounts, and record monthly payments. Managers oversee employees, products, customer accounts, and monthly business records.

---

## Features

### Manager
- Add and view employees (Operators & Recovery Collectors)
- View all customer accounts with search and status filters (Active / Dead)
- View monthly business records (new accounts, cleared accounts, recovered installments, etc.)
- Add and view products in the catalog
- View customers assigned to a specific employee

### Operator
- Register **new customers** (with guarantor details) and create installment accounts
- Register **existing customers** for new product purchases
- Record monthly installment payments
- View customer and account details by CNIC or Account Number

### Installment Plans
| Duration | Markup on Net Amount |
|----------|----------------------|
| 3 months | 20%                  |
| 6 months | 30%                  |
| 9 months | 40%                  |
| 12 months| 50%                  |

Total amount, remaining balance, and monthly payable are calculated automatically based on the selected plan and advance payment.

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Frontend   | Python, PyQt5           |
| Database   | MySQL                   |
| UI Design  | Qt Designer (`.ui` files) |
| DB Driver  | `mysql-connector-python`|

---

## Project Structure

```
Installement-Management-System-IMS/
│
├── Code/
│   ├── main.py                 # Application entry point & business logic
│   └── UI/                     # Qt Designer UI files and generated modules
│       ├── mainwindow.ui       # Welcome / landing screen
│       ├── login.ui            # Login screen
│       ├── opretorWindow.ui    # Operator dashboard
│       ├── managerWindow.ui    # Manager dashboard
│       ├── clientForm.ui       # New customer registration
│       ├── ExistedCustomer.ui  # Existing customer purchase flow
│       ├── addInstallment.ui   # Record installment payments
│       ├── addEmployee.ui      # Add employee
│       ├── veiwEmployee.ui     # View employees
│       ├── viewCustomerWindow.ui
│       ├── AddProduct.ui
│       ├── Records.ui
│       └── ...                 # Additional UI and `ui_*.py` files
│
└── Schema/
    ├── Schema.sql              # Database schema, tables, and seed data
    └── stored_procedure.sql    # MySQL stored procedures
```

---

## Database Schema

The database `InstallementManagementSystem` includes the following main entities:

| Table               | Description                                      |
|---------------------|--------------------------------------------------|
| `Manager`           | Manager profiles                                 |
| `Employee`          | Operators and recovery collectors                |
| `Customer`          | Customer personal and financial information      |
| `Guarantor`         | Guarantor details linked to customers            |
| `Product`           | Products available for installment purchase      |
| `Account`           | Installment accounts linking customers & products|
| `Payment`           | Payment breakdown (net, total, advance, monthly) |
| `Balance`           | Running balance (paid vs. remaining)             |
| `Installement`      | Individual installment payment records           |
| `InstallementRecord`| Tracks total and remaining installments          |
| `ShareHolder`       | Shareholder information                          |
| `YearlyProfit`      | Yearly profit records                            |
| `RecoveryDetail`    | Monthly recovery targets and amounts             |
| `operator_accounts` | Operator login credentials                       |
| `manager_accounts`  | Manager login credentials                        |

### Stored Procedures (`stored_procedure.sql`)
- `show_total_installements` — Installment history for an account
- `show_installement_details` — Account and customer installment details
- `show_customer_info` — Customer info by account number
- `show_customer_under_emp` — Customers handled by a specific employee

---

## Prerequisites

- **Python 3.7+**
- **MySQL Server** (e.g., MySQL Workbench)
- **pip** (Python package manager)

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Installement-Management-System-IMS.git
cd Installement-Management-System-IMS
```

### 2. Set up the database
1. Open **MySQL Workbench** (or any MySQL client).
2. Run `Schema/Schema.sql` to create the database, tables, and sample data.
3. Run `Schema/stored_procedure.sql` to create the stored procedures.

### 3. Install Python dependencies
```bash
pip install PyQt5 mysql-connector-python
```

### 4. Configure database connection
Update the MySQL connection settings in `Code/main.py`:

```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="InstallementManagementSystem"
)
```

### 5. Run the application
```bash
cd Code
python main.py
```

---

## Default Login Credentials

| Role     | Username   | Password     |
|----------|------------|--------------|
| Manager  | `yameen12` | `Yameen@123` |
| Operator | `Asad`     | `1234`       |

> Select the **Manager** checkbox on the login screen when signing in as a manager.

---

## Usage

1. Launch the application and click **Login** on the welcome screen.
2. Sign in as **Manager** or **Operator** using the credentials above.
3. **Operators** can register customers, create installment accounts, and record payments.
4. **Managers** can manage employees, products, view customer records, and monitor monthly statistics.

---

## Sample Data

The schema includes sample records for:
- Products: `MotorBike`, `Fan`
- Manager: `Ahsan`
- Employee: `Taimoor Sardar`
- Customer: `Ahsan Sajjad`

---

## Authors

NUST — Database Course Project

---

## License

This project is for academic purposes.
