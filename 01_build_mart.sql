-- Drop the table if it already exists to ensure we start fresh
DROP TABLE IF EXISTS mart_performance;

-- Create our final analysis table by joining the raw tables
CREATE TABLE mart_performance AS
SELECT
    o.order_id,
    o.order_timestamp,
    DATE(o.order_timestamp) AS order_date,
    o.order_amount,
    o.delivery_time_minutes,
    o.customer_rating_food,
    c.customer_id,
    c.city,
    c.signup_date,
    r.restaurant_id,
    r.restaurant_name,
    r.cuisine,
    r.zone
FROM
    raw_orders o
LEFT JOIN
    raw_customers c ON o.customer_id = c.customer_id
LEFT JOIN
    raw_restaurants r ON o.restaurant_id = r.restaurant_id;
	TRUNCATE raw_orders, raw_customers, raw_restaurants;
COPY raw_customers FROM 'C:/New folder/data/customers.csv' DELIMITER ',' CSV HEADER;
COPY raw_restaurants FROM 'C:/New folder/data/restaurants.csv' DELIMITER ',' CSV HEADER;
COPY raw_orders FROM 'C:/New folder/data/orders.csv' DELIMITER ',' CSV HEADER;