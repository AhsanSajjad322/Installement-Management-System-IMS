CREATE DATABASE IF NOT EXISTS InstallementManagementSystem;
USE InstallementManagementSystem;

CREATE TABLE ShareHolder (
    S_CNIC VARCHAR(15) NOT NULL,
    Name VARCHAR(30) NOT NULL,
    `%Share` INT NOT NULL,
    Address VARCHAR(100) NOT NULL,
    CONSTRAINT pk_ShareHolder PRIMARY KEY (S_CNIC)
);
    
CREATE TABLE YearlyProfit (
    Year INT NOT NULL,
    Profit FLOAT,
    CONSTRAINT pk_MonthlyProfit PRIMARY KEY (Year)
);

CREATE TABLE Earn (
    S_CNIC VARCHAR(15),
    Year INT NOT NULL,
    CONSTRAINT fk_S_CNIC FOREIGN KEY (S_CNIC)
        REFERENCES ShareHolder (S_CNIC),
    CONSTRAINT fk_Year FOREIGN KEY (Year)
        REFERENCES YearlyProfit (Year),
    CONSTRAINT pk_Earn PRIMARY KEY (S_CNIC , Year)
);

CREATE TABLE Manager (
    M_ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(30) NOT NULL,
    CNIC VARCHAR(15) NOT NULL,
    Salary INT NOT NULL,
    WorkHours INT NOT NULL,
    Address VARCHAR(100),
    CONSTRAINT pk_Manager PRIMARY KEY (M_ID)
)  AUTO_INCREMENT=10;

CREATE TABLE Employee (
    E_ID INT NOT NULL AUTO_INCREMENT,
    M_ID INT NOT NULL DEFAULT 10,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20),
    CNIC VARCHAR(15) NOT NULL,
    Salary INT NOT NULL,
    WorkHours INT NOT NULL,
    Address VARCHAR(100),
    DOB VARCHAR(20),
    Gender VARCHAR(1),
    FatherName VARCHAR(30),
    Designation VARCHAR(30),
    PhoneNo VARCHAR(20) NOT NULL,
    Martial_status VARCHAR(25) NOT NULL,
    CONSTRAINT fk_M_ID FOREIGN KEY (M_ID)
        REFERENCES Manager (M_ID),
    CONSTRAINT pk_RecoveryCollector PRIMARY KEY (E_ID)
)  AUTO_INCREMENT=15;

CREATE TABLE Product (
    ProductName VARCHAR(30) NOT NULL,
    Category VARCHAR(30),
    Price INT NOT NULL,
    CONSTRAINT pk_Product PRIMARY KEY (ProductName)
);

CREATE TABLE Customer (
    C_ID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(20),
    Address VARCHAR(100) NOT NULL,
    CNIC VARCHAR(15) NOT NULL,
    PhoneNo VARCHAR(15),
    MobileNo VARCHAR(15),
    MonthlyIncome INT NOT NULL,
    FatherName VARCHAR(30),
    MartialStatus VARCHAR(15),
    Gender VARCHAR(1),
    DOB VARCHAR(20),
    PlaceOfWork VARCHAR(100),
    CONSTRAINT pk_Customer PRIMARY KEY (C_ID)
)  AUTO_INCREMENT=100;

CREATE TABLE Account (
    AccountNo INT NOT NULL AUTO_INCREMENT,
    E_ID INT NOT NULL,
    C_ID INT NOT NULL,
    ProductName VARCHAR(30),
    DateOfCreation VARCHAR(20),
    ExpectedDuration VARCHAR(20),
    Status VARCHAR(10),
    CONSTRAINT pk_Account PRIMARY KEY (AccountNo),
    CONSTRAINT fk_R_ID FOREIGN KEY (E_ID)
        REFERENCES Employee (E_ID),
    CONSTRAINT fk_C_ID FOREIGN KEY (C_ID)
        REFERENCES Customer (C_ID),
    CONSTRAINT fk_ProductName FOREIGN KEY (ProductName)
        REFERENCES Product (ProductName)
);

CREATE TABLE Guarantor (
    G_CNIC VARCHAR(15) NOT NULL,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    Address VARCHAR(100) NOT NULL,
    PhoneNo VARCHAR(15),
    MobileNo VARCHAR(15),
    Relation VARCHAR(30) NOT NULL,
    PlaceOfWork VARCHAR(50) NOT NULL,
    CONSTRAINT pk_Guarantor PRIMARY KEY (G_CNIC)
);

CREATE TABLE GuarantiedBy (
    C_ID INT NOT NULL,
    G_CNIC VARCHAR(15) NOT NULL,
    CONSTRAINT fk_CID FOREIGN KEY (C_ID)
        REFERENCES Customer (C_ID),
    CONSTRAINT fk_G_CNIC FOREIGN KEY (G_CNIC)
        REFERENCES Guarantor (G_CNIC),
    CONSTRAINT pk_Guarantor PRIMARY KEY (C_ID , G_CNIC)
);

CREATE TABLE Payment (
    AccountNo INT NOT NULL,
    DateOfPurchased VARCHAR(20),
    NetAmount INT NOT NULL,
    TotalAmount INT NOT NULL,
    Advance INT,
    RemainingBalance INT,
    MonthlyPayable INT,
    CONSTRAINT fk_AccountNo FOREIGN KEY (AccountNo)
        REFERENCES Account (AccountNo),
    CONSTRAINT pk_Payment PRIMARY KEY (DateOfPurchased , AccountNo)
);

CREATE TABLE Balance (
    AccountNo INT NOT NULL,
    DateofInstallement VARCHAR(20),
    AmountRemaining INT,
    AmountPaid INT,
    CONSTRAINT fk_CID_Balance FOREIGN KEY (AccountNo)
        REFERENCES Account (AccountNo),
    CONSTRAINT pk_Balance PRIMARY KEY (DateOfInstallement , AccountNo)
);

CREATE TABLE Installement (
    AccountNo INT NOT NULL,
    InstallementNo INT NOT NULL,
    InstallementAmount INT NOT NULL,
    ReceivedInstallementDate VARCHAR(20),
    CONSTRAINT fk_AccountNo_Inst FOREIGN KEY (AccountNo)
        REFERENCES Account (AccountNo),
    CONSTRAINT pk_Installement PRIMARY KEY (InstallementNo , AccountNo)
);

CREATE TABLE RecoveryDetail (
    Month VARCHAR(15) NOT NULL,
    TargetedAmount INT,
    RecoveredAmount INT,
    AmountToRecover INT,
    CONSTRAINT pk_RecoveryDetail PRIMARY KEY (Month)
);

CREATE TABLE Responsible (
    E_ID INT NOT NULL,
    Month VARCHAR(15) NOT NULL,
    CONSTRAINT fk_R_ID_Res FOREIGN KEY (E_ID)
        REFERENCES Employee (E_ID),
    CONSTRAINT fk_Month FOREIGN KEY (Month)
        REFERENCES RecoveryDetail (Month),
    CONSTRAINT pk_Responsible PRIMARY KEY (E_ID , Month)
);

CREATE TABLE InstallementRecord (
    AccountNo INT,
    RemainingInstallements INT,
    TotalInstallements INT,
    CONSTRAINT fk_Installment FOREIGN KEY (AccountNo)
        REFERENCES Account (AccountNo),
    CONSTRAINT pk_InstallmentRecords PRIMARY KEY (AccountNo)
);

CREATE TABLE operator_accounts (
    user_name VARCHAR(25),
    password VARCHAR(50)
);

INSERT INTO operator_accounts VALUES('Asad','1234');
CREATE TABLE manager_accounts (
    user_name VARCHAR(25),
    password VARCHAR(50)
);
INSERT INTO manager_accounts VALUES('yameen12','Yameen@123');
INSERT INTO Product VALUES('MotorBike','Electronics',50000);
INSERT INTO Product VALUES('Fan','Electronics',10000);



INSERT INTO MANAGER VALUES(10,'Ahsan', '3840265268501','100000',6,'Qartaba Town');
INSERT INTO Employee(E_ID,FirstName,LastName,CNIC,Salary,WorkHours, Address, DOB, Gender, FatherName, Designation,PhoneNo,Martial_Status)
  VALUES(100,'Taimoor', 'Sardar', '3840265268502', 40000, 8, 'Sargodha', '2000-09-12', 'M', 'Sardar Sb', 'RC','03237008382','Single');
INSERT INTO Customer(FirstName,LastName,Address,CNIC,PhoneNo,MobileNo,MonthlyIncome,FatherName, MartialStatus, Gender, DOB, PlaceOfWork)
  VALUES('Ahsan', 'Sajjad','NUST', '123456', '049304930','3434345',2000,'Sajjad','Single','M','27/08/2003','NUST');


-- Authorization in IMS

CREATE USER 'manager'@'localhost' IDENTIFIED BY 'manager';
-- GRANT ALL ON installementmanagementsystem.* TO 'manager'@'localhost'; 


 CREATE USER 'ahsan123'@'locahost' IDENTIFIED BY 'ahsan123';
Grant 'comp_operator'@'localhost' to 'ahsan123'@'locahost'; 
SHOW GRANTS FOR 'comp_operator'@'localhost'; 
SHOW GRANTS FOR 'ahsan123'@'localhost';
CREATE ROLE 'computer_operator'@'localhost';
