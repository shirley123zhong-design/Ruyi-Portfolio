-- USE _NameOfLocalDatabase_;
USE DataScienceExam;

-- Table 1, customers
CREATE TABLE customers (    
customer_id INT NOT NULL PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
gender CHAR(1) NOT NULL
	CHECK (gender IN ('F', 'M', 'O')),
birth_year INT NOT NULL
	CHECK (birth_year BETWEEN 1900 AND 2015), -- Added CHECK BETWEEN to avoid nonsense birth years
region VARCHAR(10) NOT NULL
	CHECK (region IN ('North', 'South', 'East', 'West')), -- Added CHECK since the only possible regions are North/South/East/West
signup_date DATE NOT NULL,
loyalty_tier VARCHAR(10) NOT NULL
	CHECK (loyalty_tier IN ('Basic', 'Plus', 'Premium')),
email_opt_in BIT NOT NULL DEFAULT 1 -- boolean with the default being 1 (true)
);

-- Table 2, products
CREATE TABLE products (
product_id INT NOT NULL PRIMARY KEY,
category VARCHAR(50) NOT NULL,
brand VARCHAR(50) NOT NULL,
price DECIMAL (10,2) NOT NULL
	CHECK (price >= 0) -- Set price to >= 0 so it's possible for a product to be free (like buy 3 and get 1 for free)
);

-- Table 3, orders
CREATE TABLE orders (
order_id INT NOT NULL PRIMARY KEY,
customer_id INT	NOT NULL,
order_date DATE NOT NULL,
payment_method VARCHAR(10) NOT NULL,
total_amount DECIMAL(10,2) NOT NULL,
-- Foreign key: each order belongs to a customer
CONSTRAINT FK_orders_customers
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
-- Only allow valid payment method
CONSTRAINT CK_orders_paymentmethod
	CHECK (payment_method IN ('Card', 'PayPal', 'Transfer', 'Other')),
-- Ensure no negative totals
CONSTRAINT CK_orders_totalamount_positive
	CHECK (total_amount >= 0)
);

-- Table 4, order_items
CREATE TABLE order_items (
order_id INT NOT NULL,
product_id INT NOT NULL,
quantity INT NOT NULL,
discount_pct DECIMAL(3,2) NOT NULL, -- eg. 0.15 for 15%
-- Composite Primary Key
CONSTRAINT PK_order_items
	PRIMARY KEY (order_id, product_id),
-- Foreign key to orders
CONSTRAINT FK_order_items_orders
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
-- Foreign key to products
CONSTRAINT FK_order_items_products
    FOREIGN KEY (product_id) REFERENCES products(product_id),
-- Check constraint for valid discount range
CONSTRAINT CK_order_items_discount_pct
    CHECK (discount_pct >= 0 AND discount_pct <= 1),
-- Prevent negative or zero quantities
CONSTRAINT CK_order_items_quantity
    CHECK (quantity > 0)
 );

-- Table 5, returns (renamed order_returns)
CREATE TABLE order_returns (    
return_id INT NOT NULL PRIMARY KEY,
order_id INT NOT NULL,
product_id INT NOT NULL,
return_date DATE NOT NULL,
reason VARCHAR(30) NOT NULL
	CHECK (reason IN ('Defective', 'Size', 'Changed Mind', 'Other')),
refund_amount DECIMAL (10,2) NOT NULL
	CHECK (refund_amount >= 0),
-- Foreign key to orders
CONSTRAINT FK_returns_orders
	FOREIGN KEY (order_id) REFERENCES orders(order_id),
-- Foreign key to products
CONSTRAINT FK_returns_products
	FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Table 6, interactions
CREATE TABLE interactions (
interaction_id INT NOT NULL PRIMARY KEY,  
customer_id INT NOT NULL,
interaction_date DATE NOT NULL,  
channel VARCHAR(10) NOT NULL
	CHECK (channel IN ('Email', 'Web', 'App', 'Support')),
-- The below is only meaningful for Email, so it is allowed to be NULL (not relevant) otherwise
opened BIT NULL,
clicked BIT NULL,
-- The below is only meaningful for Web/App, so NULL is allowed
session_minutes DECIMAL (5,2) NULL,
-- The below is always 0 or 1. The default should be "not a complaint".
complaint BIT NOT NULL DEFAULT 0,
-- Foreign key to customers
CONSTRAINT FK_interactions_customers
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table 7, deliveries
CREATE TABLE deliveries (
order_id INT NOT NULL PRIMARY KEY,
shipped_date DATE NOT NULL,
delivered_date DATE NOT NULL,
on_time BIT NOT NULL,
carrier VARCHAR(10) NOT NULL
	CHECK (carrier IN ('DHL', 'UPS', 'FedEx', 'Local')),
-- Foreign key to orders
CONSTRAINT FK_deliveries_orders
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);



