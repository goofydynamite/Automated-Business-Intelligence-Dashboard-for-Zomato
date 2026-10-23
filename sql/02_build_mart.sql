-- Rebuilds the analysis-ready mart from the (already-refreshed) raw tables.
-- Must run AFTER sql/01_load_raw.sql + the CSV loads, never before.

-- mart_performance may exist as a table, view, or materialized view from
-- prior runs; drop whichever form is actually present.
DO $$
DECLARE
    obj_kind "char";
BEGIN
    SELECT relkind INTO obj_kind
    FROM pg_class
    WHERE relname = 'mart_performance'
      AND relnamespace = 'public'::regnamespace;

    IF obj_kind = 'r' THEN
        EXECUTE 'DROP TABLE mart_performance';
    ELSIF obj_kind = 'm' THEN
        EXECUTE 'DROP MATERIALIZED VIEW mart_performance';
    ELSIF obj_kind = 'v' THEN
        EXECUTE 'DROP VIEW mart_performance';
    END IF;
END $$;

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
    r.zone,
    r.zone_lat,
    r.zone_lng
FROM raw_orders o
LEFT JOIN raw_customers c   ON o.customer_id = c.customer_id
LEFT JOIN raw_restaurants r ON o.restaurant_id = r.restaurant_id;

CREATE INDEX idx_mart_order_date   ON mart_performance (order_date);
CREATE INDEX idx_mart_zone         ON mart_performance (zone);
CREATE INDEX idx_mart_restaurant   ON mart_performance (restaurant_id);
