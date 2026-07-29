--qry_T4_Question1
--Show all transactions sorted by amount, with the most expensive transactions listed first. 
--Display the year, month, cardholder name, the amount of the transaction and the vendor.  
SELECT year, Month, FullName, Amount From pcards
ORDER BY Amount DESC;

--qry_T4_Question2
--Show all transactions that occurred in the 2014 calendar year 
--sorted by month, and then, within each month, list the most expensive transactions first and then alphabetize them by the name of the employee. Display the year, month, cardholder name, the amount of the transaction and the vendor.  
SELECT year, Month, FullName, Amount From pcards
WHERE YEAR=2014
ORDER BY Month,Amount DESC,FullName;

--qry_T4_Question3
--Show all transactions that occurred in the 2014 calendar year for more than $3,000. Sort by month and then within each month list the most expensive transactions first and then alphabetize by the name of the employee. Display the year, month, cardholder name, the amount of the transaction and the vendor.  
SELECT year, Month, FullName, Amount,Vendor From pcards
WHERE YEAR=2014 AND AMOUNT>3000
ORDER BY Month,Amount DESC,FullName;

----qry_T4_Question4
--Show all transactions that came from a vendor with Amazon somewhere in the name that occurred in the 2014 calendar year that are more than $3,000. 
--Display the vendor name, employee name, amount, year and month. 
--Sort by amount so the smallest amount is listed first. 
SELECT vendor, FullName, Amount,year, Month From pcards
WHERE YEAR=2014 AND Amount>3000 AND Vendor like '%Amazon%'
ORDER BY Amount;

--qry_T4_Question5
--What is the total number of P-card transactions in the database? Label the column TotalTrans.  
SELECT COUNT(*) AS TotalTrans FROM pcards;

--qry_T4_Question6
--What is the total number of P-card transactions in the database with amounts more than or equal to $5,000? 
--Label the column TotalTransGT5k. 
SELECT COUNT(*) AS TotalTransGT5k FROM pcards
WHERE Amount>=5000;

--qry_T4_Question7
--What is the total dollar amount of transactions returned from January to March, inclusive, in 2014?  
--Label the column TotalReturns2014Q1.
SELECT SUM(Amount) AS TotalReturns2014Q FROM pcards
WHERE YEAR=2014 AND MONTH BETWEEN 1 AND 3 AND Amount<0;


----qry_T4_Question8
--What is the total number of P-card transactions in the database for each year? 
--Sort the data by year so the most recent date is listed first. Label the column with the counts as TotalTrans. 
SELECT Year, COUNT(*) AS TotalTrans
FROM pcards
GROUP BY Year
ORDER BY Year DESC;

--qry_T4_Question9
--List the names of all cardholders sorted based on who had the most transactions in the 2014 calendar year. 
--Display the name and number of transactions (labeled as NumTrans).  
SELECT FullName,COUNT(*) AS NumTrans FROM pcards
WHERE Year = 2014
GROUP BY FullName
ORDER BY NumTrans DESC;

--qry_T4_Question10
--List the names of all people and sort based on who returned the greatest dollar amount of goods in the 2014 calendar year. Display the name, total amount of returned goods (labeled as ReturnedGoodsValue) and total number of returned transactions (labeled as ReturnedGoodsCount).  
SELECT FullName, abs(SUM(Amount)) AS ReturnedGoodsValue,COUNT(*) AS ReturnedGoodsCount FROM pcards
WHERE Year = 2014 AND Amount<0
GROUP BY FullName
ORDER BY ReturnedGoodsValue DESC;

--qry_T4_Question11
--List the names of all cardholders sorted based on who had the most transactions in the 2014 calendar year. Only display cardholders who have more than 10 transactions. Display the name and number of transactions (labeled as NumTrans).  
SELECT FullName,COUNT(*) AS NumTrans FROM pcards
WHERE Year = 2014
GROUP BY FullName
HAVING NumTrans> 10
ORDER BY NumTrans DESC;

--qry_T4_Question12
--List the names of all people and sort based on who returned the greatest dollar amount of goods in the 2014 calendar year. 
--Only display people who have returned more than 1000 USD worth of goods. 
--Display the name, total amount of returned goods (labeled as ReturnedGoodsValue) and total number of returned transactions (labeled as ReturnedGoodsCount).  
SELECT FullName,ABS(SUM(Amount)) AS ReturnedGoodsValue,COUNT(*) AS ReturnedGoodsCount FROM pcards
WHERE Year = 2014 AND Amount < 0
GROUP BY FullName
HAVING ReturnedGoodsValue> 1000
ORDER BY ReturnedGoodsValue DESC;

--qry_T4_Question13
--Compute the amount of sales tax for each transaction that would have been paid if OSU were required to pay sales tax in December 2014.
--The state sales tax rate is 4.5%. Display the month, year, cardholder name, description, vendor name, amount and computed sales tax amount (labeled SalesTax). Sort by the sales tax amount so the largest items appear on the top.  
SELECT Month,Year,FullName,Description,Vendor,Amount,Amount*0.045 AS SalesTax FROM pcards
WHERE Year = 2014 AND Month = 12 AND Amount > 0
ORDER BY SalesTax DESC;

--qry_T4_Question14
--The university would like to know how much money it saved by not paying state sales tax. The state sales tax rate is 4.5%. 
--If you assume all sales are made net of the state sales tax, how much money did OSU avoid paying in sales tax to the government on P-card transactions for each calendar year? Show the year, total amount spent and total amount saved in sales tax (label as SalesTaxSaved). 
--Make sure to round dollar figures to the nearest cent using the Property Sheet, Format field (use the currency format) rather than using a formula. 
--Sort the data by year with the most recent year listed first.      
SELECT Year,SUM(Amount) AS TotalSpent,SUM(Amount)*0.045 AS SalesTaxSaved FROM pcards
WHERE Amount>0
GROUP BY Year
ORDER BY Year DESC;

--qry_T4_Question15
--Related to problem 14., the university estimates it had to pay sales tax in other states 30% of the time. 
--Reperform problem 14., but only compute the savings as 70% of the transaction totals instead of 100%. 
--Make sure to round dollar figures to the nearest cent using the Property Sheet, Format field (use the currency format) rather than using a formula.  
SELECT Year,SUM(Amount) AS TotalSpent,SUM(Amount)*0.70*0.045 AS SalesTaxSaved FROM pcards
WHERE Amount > 0
GROUP BY Year
ORDER BY Year DESC;

--qry_T4_Question16
--Compute the number of days between the transaction date and the posted date for all transactions in the month for November 2014. Display the month, year, cardholder name, description, vendor name, amount and amount of time (labeled as TimeDif). Numbers should be positive if the posted date took place after the transaction date. Sort by TimeDif and then the name of the employee so the items that took the most days appear on the top.  
SELECT Month,Year,CardholderName,Description,Vendor,Amount,julianday(PostedDate)-julianday(TransactionDate) AS TimeDif
FROM PCardTransactions
WHERE Year = 2014
  AND Month = 11
ORDER BY TimeDif DESC, CardholderName;
--I tried datediff as well, not available i sqlite.

--qry_T4_Question17
--Create a risk ranking of returned items in 2014. 
--Create a new column of data that shows whether something is high risk, medium risk or low risk based on the following criteria. If the return was equal to or more than $1,000, it is high risk; if the return is equal to or more than $500 and less than $1,000, it is medium risk; and if the return is less than $500, it is low risk. 
--Display the year, name of the cardholder, description, vendor, amount of return and the new column (labeled RiskRanking). Sort the data so that the largest returns are listed first, and do not list any data that is not a return. As a hint, remember that returns are listed as negative numbers — make sure to think about this carefully.  
SELECT Year,FullName,Description,Vendor,Amount AS ReturnAmount,
CASE WHEN ABS(Amount) >= 1000 THEN 'High Risk'
WHEN ABS(Amount) >= 500 AND ABS(Amount) < 1000 THEN 'Medium Risk'
ELSE 'Low Risk'
END 
AS RiskRanking
FROM pcards
WHERE Year = 2014 AND Amount < 0
ORDER BY ABS(Amount) DESC;


--qry_T4_Question18
--OSU potentially can earn money from Amazon.com if employees make their purchases at smile.amazon.com and direct the earnings to OSU. 
--Assume that for all transactions at the vendor Amazon.com, OSU would earn 0.75% for transactions $500 and more and 0.50% for transactions less than $500. 
--What is the total amount that OSU would earn for 2014 based on these amounts?  
--Label the column AmazonEarnings in your output.  
SELECT SUM(CASE WHEN Amount>=500 THEN Amount*0.0075
WHEN Amount<500 THEN Amount*0.005
END) AS AmazonEarnings
FROM pcards
WHERE Year=2014 AND Vendor='Amazon.com' AND Amount>0;


--These next queries require you to create multiple queries to solve them. That is, you will perform one query and then reference that query in a second (third, fourth, etc.) query to solve these problems.  
--qry_T4_Question19
--Show all 2014 transactions sorted by the amount (with the most expensive transactions listed first) that are greater than the average transaction amount for 2014. 
--Display the year, month, cardholder name, the amount of the transaction and the vendor.  
SELECT Year, Month, FullName, Amount, Vendor FROM pcards
WHERE Year = 2014 AND Amount>(
      SELECT AVG(Amount) FROM pcards
      WHERE Year = 2014)
ORDER BY Amount DESC;

--qry_T4_Question20
--List how much more or less was spent at each vendor in 2014 than in 2013. Only include companies for which there was a purchase in both 2013 and 2014. Display the vendor name and the difference in the amount spent in 2014 and 2013 (label as DiffSpending), with positive numbers indicating more was spent in 2014 than in 2013 (and sort the results so the largest increases in spending are listed at the top).  
SELECT total2014.Vendor, amount2014 - amount2013 AS DiffSpending 
FROM(SELECT Vendor, SUM(Amount) AS amount2014 FROM pcards 
WHERE Year=2014 AND Amount > 0 
GROUP BY Vendor) AS total2014 
INNER JOIN 
(SELECT Vendor, SUM(Amount) AS amount2013 FROM pcards 
WHERE Year=2013 AND Amount > 0
GROUP BY Vendor) AS total2013 
ON total2014.Vendor=total2013.Vendor 
ORDER BY DiffSpending DESC;

--qry_T4_Question21
--Show all 2014 vendors for which employees purchased more during the year than the total amount spent at the top vendor in 2013. Display the total amount of the transactions (labeled TotalSpent) and the vendor. Sort the results by the total amount of the transactions with the greater totals listed first.  
SELECT Vendor,SUM(Amount) AS TotalSpent FROM pcards
WHERE Year=2014 AND Amount>0
GROUP BY Vendor
HAVING TotalSpent>(
SELECT MAX(Total2013) FROM (
        SELECT SUM(Amount) AS Total2013
        FROM pcards
        WHERE Year = 2013
          AND Amount > 0
        GROUP BY Vendor)
)
ORDER BY TotalSpent DESC;

--qry_T4_Question22
--Create a query that calculates the percentage increase and decrease in the number of transactions for 2012, 2013 and 2014 relative to 2011. That is, the query output should provide two columns, with the first being the year (using 2012, 2013 and 2014 as rows) and the second column labeled PercDiffFrom2010, and calculate the percentage increase and decrease in transactions since 2011 as follows: (# of transactions in 201X – # of transactions in 2011) / (# of transactions in 2011)*100 and round it to two decimal spaces using the Round formula. As a hint, make sure you do not count a field that has some null values, like the Description field, because this will give you the wrong answer.  
SELECT Year,ROUND((COUNT(*)-
(SELECT COUNT(*)FROM pcards
 WHERE Year=2011)
 )*100/(SELECT COUNT(*) FROM pcards
        WHERE Year = 2011),2) AS PercDiffFrom2010
FROM pcards
WHERE Year IN (2012, 2013, 2014)
GROUP BY Year
ORDER BY Year;



--qry_T5_Question1
--User shall not spend more than $50,000 per year
--Display the name and total amount spent during the year for all employees who spent more than $50,000 in 2014.  
--Sort by the total amount spent with the larger amounts listed first.
SELECT FullName,sum(Amount) AS TotalAmountSpent FROM pcards
where YEAR=2014
GROUP BY FullName
HAVING sum(Amount)>50000
ORDER BY Amount DESC;

--qry_T5_ Question2
--User shall not spend more than $10,000 per month without approval.
--Display the name, total amount spent during the month and the month for all employees who spent more than $10,000 per month in 2014. 
--Sort by month (January listed first) and then total the amount spent with the larger amounts listed first.
SELECT FullName,sum(Amount) AS TotalAmountSpent,Month FROM pcards
WHERE year=2014
GROUP BY FullName, Month
HAVING sum(Amount)>10000
ORDER BY Month ASC, Amount DESC;

--qry_T5_ Question3	
--User shall not spend more than $5,000 per transaction.	
--Display all transaction details (Amount, Name, Description, Vendor, TransactionDate, PostedDate and MCC) for any transaction in 2014 that was for more than $5,000. 
--Sort by the total transaction amount.
SELECT FullName,Amount,Description,Vendor,TransactionDate,PostedDate,MCC FROM pcards
WHERE amount>5000 AND year=2014
GROUP BY FullName
ORDER BY Amount DESC;

--qry_T5_ Question4
--An amount more than $5,000 should not be split between two or more swipes of the card by the same person.	
--Display all transaction details where the vendor and purchaser are the same on a specific day, there is more than one transaction for the day and the combined total of the transaction was more than $5,000. 
--Sort them in ascending order by the TransactionDate
SELECT p.FullName,p.Amount,p.Description,p.Vendor,p.TransactionDate,p.PostedDate,p.MCC FROM pcards As p
JOIN(
    SELECT FullName,TransactionDate,Vendor,SUM(Amount) AS TotalAmountSpent,COUNT(*) AS TransactionCount FROM pcards
    GROUP BY FullName, Vendor, TransactionDate
    HAVING COUNT(*)>1 AND SUM(Amount) > 5000
)As SplitSpentControl
ON p.FullName=SplitSpentControl.FullName
AND p.Vendor=SplitSpentControl.Vendor
AND p.TransactionDate=SplitSpentControl.TransactionDate
WHERE Year=2014
ORDER BY p.TransactionDate ASC;

--qry_T5_ Question5 
--Purchases should not be split between two or more cardholders.
--To simplify, we only will consider splitting these between two people. 
--Display all transaction information in which the combined total for a vendor on a day was more than $5,000 and there were two different cardholders who made a purchase from that vendor (make sure the query excludes people who may have made double payments). 
--Sort them in ascending order by the TransactionDate. 
SELECT p.FullName,p.Amount,p.Description,p.Vendor,p.TransactionDate,p.PostedDate,p.MCC FROM pcards As p
JOIN(
SELECT count(DISTINCT FullName)AS purchaseNr, count(*) AS TransactNr, TransactionDate,Vendor,SUM(Amount) AS TotalAmountSpent FROM pcards
GROUP BY Vendor, TransactionDate
HAVING SUM(Amount)>5000 AND COUNT(DISTINCT FullName)=2 AND count(*)=2
)AS SplitSpent
ON p.Vendor=SplitSpent.Vendor
AND p.TransactionDate=SplitSpent.TransactionDate
WHERE Year=2014
ORDER BY p.TransactionDate ASC;


--qry_T5_ Question6
--Purchases should not be split between two or more vendors.
--To simplify, we will only consider splitting these between two vendors. 
--Display all transaction information in which the combined total for a person on a day was more than $5,000 and there were purchases made at two different vendors (make sure the query excludes people who may have made double payments at one vendor). 
--Sort them in ascending order by the TransactionDate.
SELECT p.FullName,p.Amount,p.Description,p.Vendor,p.TransactionDate,p.PostedDate,p.MCC FROM pcards As p
JOIN(
SELECT FullName, count(DISTINCT Vendor)AS vendorCount, count(*) AS TransactNr, TransactionDate,SUM(Amount) AS TotalAmountSpent FROM pcards
GROUP BY FullName, TransactionDate
HAVING SUM(Amount)>5000 AND COUNT(DISTINCT Vendor)=2 AND count(*)=2
)AS SplitVendor
ON p.FullName=SplitVendor.FullName
AND p.TransactionDate=SplitVendor.TransactionDate
WHERE Year=2014
ORDER BY p.TransactionDate ASC;

--qry_T5_Question7
--Transactions are prohibited for expenses for food and mileage while traveling. A per diem for food expenses and mileage may be claimed using a travel voucher.  
--For the days when an employee makes a purchase using an MCC that contains the words hotel, motel, resort or inn, return all transaction details about any transactions for those employees who on those days also contain MCCs that have the words food or restaurant. 
--Sort them in ascending order by name and then the amount.
SELECT p.FullName,p.Amount,p.Description,p.Vendor,p.TransactionDate,p.PostedDate,p.MCC FROM pcards As p
JOIN(
SELECT FullName, TransactionDate FROM pcards
GROUP BY FullName, TransactionDate
HAVING SUM(
CASE WHEN LOWER(MCC) LIKE '%hotel%' OR LOWER(MCC) LIKE '%motel%' OR LOWER(MCC) LIKE '%resort%' OR LOWER(MCC) LIKE '%inn%'
THEN 1 
ELSE 0
END
)>0
AND SUM(
CASE WHEN LOWER(MCC) LIKE '%food%' OR LOWER(MCC) LIKE '%restaurant%'
THEN 1 
ELSE 0
END
)>0
)AS ProhibitPurchase
ON p.FullName=ProhibitPurchase.FullName
AND p.TransactionDate=ProhibitPurchase.TransactionDate
WHERE year=2014
ORDER BY p.FullName ASC, p.Amount ASC;

--CASE WHEN CONDITION THEN VALUE IF TRUE ELSE VALUE IF FALSE END