CREATE DATABASE customer_analytics_db;
USE customer_analytics_db;
SELECT DATABASE();
SHOW TABLES;
SELECT *
FROM ecommerce_customer_churn

LIMIT 10;
SELECT Customer_ID,
       Age,
       Gender,
       Total_Spend
FROM ecommerce_customer_churn
LIMIT 10;
SELECT Customer_ID AS Customer,
       Total_Spend AS Revenue
FROM ecommerce_customer_churn 
LIMIT 10;
RENAME TABLE ecommerce_customer_churn TO customers;
SHOW TABLES;
SELECT * FROM customers
WHERE Churn = 1
  AND Total_Spend > (
      SELECT AVG(Total_Spend)
      FROM customers
  );
  SELECT COUNT(*) AS Churned_High_Value_Customers
FROM customers
WHERE Churn = 1
  AND Total_Spend > (
      SELECT AVG(Total_Spend)
      FROM customers
  );
  SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
ORDER BY Total_Spend DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
ORDER BY Total_Spend ASC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Customer_Lifetime_Value
FROM customers
ORDER BY Customer_Lifetime_Value DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Loyalty_Score
FROM customers
ORDER BY Loyalty_Score DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Age
FROM customers
where Total_Spend > (
      SELECT AVG(Total_Spend)
      FROM customers)
ORDER BY Age ASC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
WHERE Churn = 1
ORDER BY Total_Spend DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
ORDER BY Total_Spend DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Customer_Lifetime_Value
FROM customers
ORDER BY Customer_Lifetime_Value DESC
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
WHERE Churn = 1
ORDER BY Total_Spend DESC
LIMIT 10;
SELECT Membership_Type,
       COUNT(*) AS Total_Customers
FROM customers
GROUP BY Membership_Type;
SELECT Membership_Type,
       COUNT(*) AS Total_Customers
FROM customers
GROUP BY Membership_Type;
SELECT Membership_Type,
       SUM(Total_Spend) AS Total_Revenue
FROM customers
GROUP BY Membership_Type;
SELECT State,
       SUM(Total_Spend) AS Total_Revenue
FROM customers
GROUP BY State ORDER BY Total_Revenue DESC;
SELECT Membership_Type,
       AVG(Total_Spend) AS Avg_Spend
FROM customers
GROUP BY Membership_Type
HAVING AVG(Total_Spend) > 100;
SELECT State,
       COUNT(*) AS Total_Customers
FROM customers
GROUP BY State
HAVING COUNT(*) > 2000;
SELECT Membership_Type,
       SUM(Total_Spend) AS Total_Revenue
FROM customers
GROUP BY Membership_Type
HAVING SUM(Total_Spend) > 10000000;
SELECT Membership_Type,
       AVG(Total_Spend) AS Avg_Spend
FROM customers
WHERE Churn = 1
GROUP BY Membership_Type
HAVING AVG(Total_Spend) > 1000;
SELECT Customer_ID,
       Full_Name,
       Total_Spend,
       ROW_NUMBER() OVER (ORDER BY Total_Spend DESC) AS Row_Num
FROM customers
LIMIT 10;
SELECT Customer_ID,
       Full_Name,
       Membership_Type,
       Total_Spend,
       ROW_NUMBER() OVER (
           PARTITION BY Membership_Type
           ORDER BY Total_Spend DESC
       ) AS Rank_No
FROM customers;
SELECT Membership_Type,
       AVG(Total_Spend) AS Avg_Spend
FROM customers
GROUP BY Membership_Type
HAVING AVG(Total_Spend) > 5000;
SELECT State,
       COUNT(*) AS Total_Customers
FROM customers
GROUP BY State
HAVING COUNT(*) > 2000;
SELECT Customer_ID,
       Full_Name,
       Age,
       CASE
           WHEN Age <= 25 THEN 'Young'
           WHEN Age BETWEEN 26 AND 40 THEN 'Adult'
           WHEN Age BETWEEN 41 AND 55 THEN 'Middle Age'
           ELSE 'Senior'
       END AS Age_Group
FROM customers
LIMIT 20;
CREATE TABLE orders (
    Order_ID INT PRIMARY KEY,
    Customer_ID VARCHAR(20),
    Product_Name VARCHAR(50),
    Order_Amount DECIMAL(10,2)
);
INSERT INTO orders VALUES
(101,'CUST1001','Laptop',65000),
(102,'CUST1002','Mobile',25000),
(103,'CUST1003','Headphone',3000),
(104,'CUST1001','Keyboard',2000),
(105,'CUST1005','Monitor',18000);
SELECT *
FROM orders;
SELECT * FROM orders;
SELECT c.Customer_ID,
       c.Full_Name,
       c.Age,
       o.Product_Name,
       o.Order_Amount
FROM customers c
INNER JOIN orders o
ON c.Customer_ID = o.Customer_ID;
SELECT c.Full_Name,
       o.Product_Name,
       o.Order_Amount
FROM customers c
INNER JOIN orders o
ON c.Customer_ID = o.Customer_ID
ORDER BY o.Order_Amount DESC;
SELECT Customer_ID
FROM customers
LIMIT 10;
DELETE FROM orders;
INSERT INTO orders VALUES
(101,'CUST000001','Laptop',65000),
(102,'CUST000002','Mobile',25000),
(103,'CUST000003','Headphone',3000),
(104,'CUST000001','Keyboard',2000),
(105,'CUST000005','Monitor',18000);
SELECT * FROM orders;
SELECT Customer_ID,
       Full_Name,
       Total_Spend
FROM customers
WHERE Churn = 1;
CREATE INDEX idx_customer_id
ON customers(Customer_ID);
CREATE INDEX idx_customer_id
ON customers(Customer_ID(20));
DESCRIBE customers;
ALTER TABLE customers
MODIFY Customer_ID VARCHAR(20);
SHOW INDEX
FROM customers;
CREATE INDEX idx_customer_id
ON customers(Customer_ID);
EXPLAIN
SELECT *
FROM customers
WHERE State='Tamil Nadu';