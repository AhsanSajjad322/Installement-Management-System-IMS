
-- ------------------------------------------------------STORED PROCEDURE 1 --------------------------------------------------------------
USE `installementmanagementsystem`;
DROP procedure IF EXISTS `show_total_installements`;

USE `installementmanagementsystem`;
DROP procedure IF EXISTS `installementmanagementsystem`.`show_total_installements`;
;

DELIMITER $$
USE `installementmanagementsystem`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `show_total_installements`(IN id INT)
BEGIN
SELECT 
    I.InstallementNo,
    I.ReceivedInstallementDate,
    Balance.AmountPaid,
    Balance.AmountRemaining,
    IR.RemainingInstallements
FROM
    Installement I
        JOIN
    InstallementRecord IR USING (AccountNo)
        JOIN
    Balance USING (AccountNo)
WHERE
    AccountNo = id;
END$$

DELIMITER ;
;

-- ------------------------------------------------------STORED PROCEDURE 2 --------------------------------------------------------------
USE `installementmanagementsystem`;
DROP procedure IF EXISTS `show_installement_details`;

USE `installementmanagementsystem`;
DROP procedure IF EXISTS `installementmanagementsystem`.`show_installement_details`;
;

DELIMITER $$
USE `installementmanagementsystem`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `show_installement_details`(IN Id INT)
BEGIN
SELECT 
    CONCAT(Customer.FirstName,
            ' ',
            Customer.LastName),
    Account.ProductName,
    Product.Price,
    Balance.AmountRemaining,
    InstallementRecord.RemainingInstallements
FROM
    Account
        JOIN
    Customer USING (C_ID)
        JOIN
    Payment USING (AccountNo)
        JOIN
    Product USING (ProductName)
        JOIN
    Balance USING (AccountNo)
        JOIN
    InstallementRecord USING (AccountNo)
WHERE
    AccountNo = Id;

END$$

DELIMITER ;
;



-- ------------------------------------------------------STORED PROCEDURE 3 --------------------------------------------------------------

USE `installementmanagementsystem`;
DROP procedure IF EXISTS `show_customer_info`;

DELIMITER $$
USE `installementmanagementsystem`$$
CREATE PROCEDURE `show_customer_info` (IN id INT)
BEGIN
SELECT 
    AccountNo,
    C_ID,
    CONCAT(FirstName, ' ', LastName),
    ProductName,
    MobileNo,
    MonthlyIncome,
    gender,
    status,
    PlaceOfWork
FROM
    account
        JOIN
    customer USING (C_ID)
WHERE
    AccountNo = id;
END$$

DELIMITER ;


USE `installementmanagementsystem`;
DROP procedure IF EXISTS `show_customer_under_emp`;
-- ------------------------------------------------------STORED PROCEDURE 4 --------------------------------------------------------------

USE `installementmanagementsystem`;
DROP procedure IF EXISTS `show_customer_under_emp`;

USE `installementmanagementsystem`;
DROP procedure IF EXISTS `installementmanagementsystem`.`show_customer_under_emp`;
;

DELIMITER $$
USE `installementmanagementsystem`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `show_customer_under_emp`(IN id INT)
BEGIN
SELECT 
	AccountNo,
    CONCAT(FirstName, ' ', LastName),
    ProductName,
    TotalAmount,
    AmountPaid,
    MonthlyPayable,
    TotalInstallements,
    RemainingInstallements
FROM
    account
        NATURAL JOIN
    customer
        NATURAL JOIN
    payment
        NATURAL JOIN
    installementrecord
        NATURAL JOIN
    balance
WHERE
    E_ID = id;
END$$

DELIMITER ;
;



