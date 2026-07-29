USE DataScienceExam;

--Ruyi Zhong
--Customer Segmentation (2 questions)
--1. What is the age distribution of customers within each loyalty tier?
--(Age groups: 0–17, 18–34, 35–49, 50-65, 65+)

    --create temporary table to check age
WITH customer_ages AS (
    SELECT
        customer_id,
        loyalty_tier,
        YEAR(GETDATE()) - birth_year AS age
    FROM customers
),
    --second temporary table,  based on the first one, to create age table
    --I choose to seperate as minors, youth,easlier career,established career(family stage),mature adults,seniors
    --select from loyalty_tier,CASE(conditional logic block)assign customer to age bucket
age_buckets AS (
    SELECT
        loyalty_tier,
        CASE
            WHEN (YEAR(GETDATE()) - birth_year) < 17 THEN '0-17'
            WHEN (YEAR(GETDATE()) - birth_year) BETWEEN 18 AND 24 THEN '18-24'
            WHEN (YEAR(GETDATE()) - birth_year) BETWEEN 25 AND 34 THEN '25-34'
            WHEN (YEAR(GETDATE()) - birth_year) BETWEEN 35 AND 49 THEN '35-49'
            WHEN (YEAR(GETDATE()) - birth_year) BETWEEN 50 AND 64 THEN '50-65'
            ELSE '65+'
        END AS age_group
    FROM customers
)
SELECT
    age_group,
    loyalty_tier,
    COUNT(*) AS customer_count
FROM age_buckets
GROUP BY age_group, loyalty_tier
ORDER BY age_group, loyalty_tier;

--2. What is the gender distribution within each loyalty tier?
SELECT
    loyalty_tier,
    gender,
    COUNT(*) AS customer_count,
    100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY loyalty_tier) AS pct_within_tier
FROM customers
GROUP BY loyalty_tier, gender
ORDER BY loyalty_tier, gender;

--3. What is the average quantity of items per order across all customers?
WITH order_item_totals AS (
    SELECT
        order_id,
        SUM(quantity) AS total_quantity_in_order
    FROM order_items
    GROUP BY order_id
)
SELECT
    AVG(CAST(total_quantity_in_order AS FLOAT)) AS avg_items_per_order
FROM order_item_totals;

--4.For each tier of customer, what is the most frequent quantity for each order?
    --first CTE, temporary table for counting loyalty tier numbers
    --second CTE, temporary table for rank quantities by frequency within each tier.
    --sorted in the end by rank
WITH qty_counts AS (
    SELECT
        c.loyalty_tier,
        oi.quantity,
        COUNT(*) AS cnt
    FROM order_items oi
    JOIN orders o       ON oi.order_id = o.order_id
    JOIN customers c    ON o.customer_id = c.customer_id
    GROUP BY c.loyalty_tier, oi.quantity
),
ranked AS (
    SELECT
        loyalty_tier,
        quantity,
        cnt,
        ROW_NUMBER() OVER (PARTITION BY loyalty_tier ORDER BY cnt DESC) AS rn
    FROM qty_counts
)
SELECT
    loyalty_tier,
    quantity AS most_common_quantity,
    cnt     AS occurrences
FROM ranked
WHERE rn = 1
ORDER BY loyalty_tier;

--5.List all products with their profit per unit (approx. net revenue per unit)
SELECT
    p.product_id,
    p.category,
    p.brand,
    p.price AS profit_per_unit,          
    RANK() OVER (ORDER BY p.price DESC) AS profit_per_unit_rank
FROM products AS p
ORDER BY profit_per_unit_rank, p.product_id;


--6,List and rank all products’ total profit
    --build one CTE: total quantity sold and total profit per product
    -- than rank
    WITH product_profit AS (
    SELECT
        p.product_id,
        p.category,
        p.brand,
        p.price AS profit_per_unit,            
        SUM(oi.quantity) AS total_quantity_sold,
        SUM(oi.quantity * p.price) AS total_profit
    FROM order_items AS oi
    JOIN products AS p
        ON oi.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.category,
        p.brand,
        p.price
)
SELECT
    product_id,
    category,
    brand,
    profit_per_unit,
    total_quantity_sold,
    total_profit,
    RANK() OVER (ORDER BY total_profit DESC) AS total_profit_rank
FROM product_profit
ORDER BY total_profit_rank, product_id;

--7, What percentage of customers have submitted at least one complaint, and how many total complaints were recorded?
    -- CTE table for each customer complains number
    -- CTE table for customer count
    -- Cross join for 1 row each table and calculate percentage
WITH complaints AS (
    SELECT
        COUNT(*) AS total_complaint_interactions,
        COUNT(DISTINCT customer_id) AS customers_with_complaints
    FROM interactions
    WHERE complaint = 1
),
customer_counts AS (
    SELECT COUNT(*) AS total_customers
    FROM customers
)
SELECT
    total_complaint_interactions,
    customers_with_complaints,
    total_customers,
    100.0 * customers_with_complaints / total_customers AS pct_customers_with_complaint
FROM complaints
CROSS JOIN customer_counts;

--8,What percentage of deliveries were not completed on time?
SELECT
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN on_time = 0 THEN 1 ELSE 0 END) AS late_deliveries,
    100.0 * SUM(CASE WHEN on_time = 0 THEN 1 ELSE 0 END) / COUNT(*) AS pct_deliveries_not_on_time
FROM deliveries;

-- Sasja Stein
-- Loyalty Tier Insights
    -- 1) Average order value by loyalty tier
SELECT
    c.loyalty_tier,
    COUNT(DISTINCT c.customer_id) AS customer_count, -- Number of customers per loyalty tier
    COUNT(o.order_id) AS order_count, -- Number of orders
    AVG(o.total_amount) AS avg_order_value, -- Average order value
    SUM(o.total_amount) AS total_revenue -- Total revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.loyalty_tier;

-- Product Insights
    -- 2) Top 10 products sold by quantity
SELECT TOP 10
    p.product_id,
    p.category,
    p.brand,
    p.price,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * p.price), 2) AS est_gross_sales,
    COUNT(DISTINCT oi.order_id) AS orders_containing_product,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
GROUP BY p.product_id, p.category, p.brand, p.price
ORDER BY total_units_sold DESC;

    -- 3) Which product is the most popular (most sold) within each loyalty tier?
WITH tier_product_sales AS (
    SELECT
        c.loyalty_tier,
        p.product_id,
        p.category,
        p.brand,
        p.price,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.quantity * p.price) AS revenue,
        ROW_NUMBER() OVER (
            PARTITION BY c.loyalty_tier
            ORDER BY SUM(oi.quantity) DESC
        ) AS rank_in_tier
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY
        c.loyalty_tier, p.product_id, p.category, p.brand, p.price
)
SELECT
    loyalty_tier,
    product_id,
    category,
    brand,
    price,
    units_sold,
    revenue
FROM tier_product_sales
WHERE rank_in_tier = 1
ORDER BY loyalty_tier;

-- Payment Method Insights
    -- 4) Revenue by Payment Method
SELECT
    payment_method,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY payment_method;

    -- 5) Payment Method vs Email opt-in
SELECT
    o.payment_method,
    c.email_opt_in,
    COUNT(*) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    CAST(AVG(o.total_amount) AS DECIMAL(12,2)) AS avg_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY o.payment_method, c.email_opt_in
ORDER BY o.payment_method, c.email_opt_in DESC;

-- Regional and Deliverance Insights
    -- 6) Customers and orders by region
SELECT
    c.region,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY c.region;

    -- 7) How many delayed deliveries are there in each region?
SELECT
    c.region,
    COUNT(*) AS delayed_deliveries
FROM deliveries d
JOIN orders o
    ON d.order_id = o.order_id
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE d.on_time = 0
GROUP BY c.region
ORDER BY delayed_deliveries DESC;

    -- 8) Are complaints more common for late deliveries, and does it vary by region?
SELECT
    c.region,
    d.on_time,
    COUNT(*) AS total_deliveries,
    COUNT(CASE WHEN i.complaint = 1 THEN 1 END) AS complaints,
    CAST(
        COUNT(CASE WHEN i.complaint = 1 THEN 1 END) * 1.0
        / COUNT(*)
        AS DECIMAL(5,4)
    ) AS complaint_rate
FROM deliveries d
JOIN orders o
    ON d.order_id = o.order_id
JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN interactions i
    ON c.customer_id = i.customer_id
   AND i.channel = 'Support'
GROUP BY c.region, d.on_time
ORDER BY c.region, d.on_time;

-- Svetlana Podolskaja
-- 1. Is there a big time difference between order and shipping date by region of the customer?
    -- If so, it may come due to some technical issues that we need to tackle, for example,
    -- understocking in the warehouses, inefficient partnership with shipping companies, etc.
SELECT
    c.region,
    AVG(CAST(d.on_time AS float))AS on_time_rate,
    SUM(CASE WHEN d.on_time = 0 THEN 1 ELSE 0 END) AS late_deliveries,
    COUNT(*) AS total_deliveries
FROM deliveries d
JOIN orders o ON d.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY on_time_rate ASC;

-- 2. Did the customer place a new order after leaving a complaint through Support?
    -- Can be one of the KPI’s for Customer Support department.
SELECT
  c.customer_id,
  i.interaction_date AS complaint_date,
  MIN(o2.order_date) AS first_order_after_complaint
FROM interactions i
JOIN customers c
  ON i.customer_id = c.customer_id
LEFT JOIN orders o2
  ON o2.customer_id = c.customer_id
  AND o2.order_date > i.interaction_date
WHERE i.channel = 'Support'
GROUP BY c.customer_id, i.interaction_date
HAVING MIN(o2.order_date) IS NOT NULL;

-- 3. Is email channel effective among young customers (between 1997 and 2010 birth year)?
    -- Shows if this marketing tool is beneficial among generation Z, or should we proceed with other more accurate solutions.
SELECT
 COUNT(*) AS email_clicks_young_customers
FROM interactions i
JOIN customers c
ON i.customer_id = c.customer_id
WHERE i.channel = 'Email'
 AND i.clicked = 1
 AND c.birth_year BETWEEN 1997 AND 2010;

-- 4. How many orders have been placed on the same day as interaction with our promotion channels happened?
    -- After grouping, demonstrates the most efficient marketing channels.
SELECT
 c.customer_id,
 o.order_id,
 o.order_date,
 i.channel,
 i.opened AS email_opened,
 i.session_minutes,
CASE
 WHEN i.channel = 'Email' AND i.opened = 1 THEN 'Email Opened'
 WHEN i.channel IN ('Web', 'App') AND i.session_minutes > 0 THEN 'Web/App
Session'
 ELSE 'Other'
END AS interaction_type
FROM orders o
JOIN interactions i
ON o.customer_id = i.customer_id
AND o.order_date = i.interaction_date
JOIN customers c
ON c.customer_id = o.customer_id
ORDER BY o.order_date, c.customer_id;

-- 5. Are there any products which are being returned more often than kept?
    -- If yes, we would probably need to examine them, especially, if this happens due to the product being Defective.
SELECT *
FROM (
    SELECT
        oi.product_id,
        COUNT(*) AS total_purchased,
        SUM(CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END) AS total_returned
    FROM order_items oi
    LEFT JOIN order_returns r
        ON oi.order_id = r.order_id
       AND oi.product_id = r.product_id
    GROUP BY oi.product_id
) t
WHERE total_returned > (total_purchased - total_returned)
ORDER BY total_returned DESC;

-- 6. Do the orders with bigger difference between order and shipping date have more returns, where the reason wouldn’t be Defect or Size?
    -- Could we possibly minimize the amount of returned orders by optimising the speed of shipping?
SELECT
  CASE
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 1 THEN '0-1 days'
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 3 THEN '2-3 days'
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 7 THEN '4-7 days'
    ELSE '8+ days'
  END AS delay_bucket,
  COUNT(*) AS total_orders,
  SUM(CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END) AS non_defect_non_size_returns,
  1.0 * SUM(CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) AS return_rate
FROM orders o
JOIN deliveries d
  ON o.order_id = d.order_id
LEFT JOIN order_items oi
  ON o.order_id = oi.order_id
LEFT JOIN order_returns r
  ON r.order_id = oi.order_id
  AND r.product_id = oi.product_id
  AND r.reason NOT IN ('Defect', 'Size')
GROUP BY
  CASE
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 1 THEN '0-1 days'
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 3 THEN '2-3 days'
    WHEN DATEDIFF(day, o.order_date, d.shipped_date) <= 7 THEN '4-7 days'
    ELSE '8+ days'
  END
ORDER BY return_rate DESC;

-- 7. Are there any customers repeatedly ordering the same products in large amounts?
    -- A possibility to build stronger connections and increase customer loyalty by further customised suggestions and special offers.
WITH customer_product_orders AS (
SELECT
 o.customer_id,
 oi.product_id,
 SUM(oi.quantity) AS total_quantity,
 COUNT(DISTINCT o.order_id) AS num_orders
FROM orders o
JOIN order_items oi
 ON o.order_id = oi.order_id
GROUP BY o.customer_id, oi.product_id
)

SELECT
 c.customer_id,
 p.product_id,
 p.category,
 p.brand,
 cpo.total_quantity,
 cpo.num_orders
FROM customer_product_orders cpo
JOIN products p
ON p.product_id = cpo.product_id
JOIN customers c
ON c.customer_id = cpo.customer_id
WHERE cpo.num_orders > 1 -- ordered repeatedly
 AND cpo.total_quantity >= 3 -- large total amount
ORDER BY cpo.total_quantity DESC, cpo.num_orders DESC;
-- 8. Are there a lot of return due to Size?
-- If this is the case in more then 50%, should we change or add the size table,
-- or add a bigger button to double check size in order to minimise return cases in the future.
SELECT
 p.category,
 COUNT(*) AS size_returns
FROM order_returns r
JOIN products p
ON r.product_id = p.product_id
WHERE r.reason = 'Size'
GROUP BY p.category
ORDER BY size_returns DESC;
