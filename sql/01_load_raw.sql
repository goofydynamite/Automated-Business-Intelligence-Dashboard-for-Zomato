-- Clears staging tables before a fresh load.
-- Children (raw_orders) must be truncated before parents due to FKs.
TRUNCATE TABLE raw_orders, raw_customers, raw_restaurants RESTART IDENTITY CASCADE;

-- Actual data loading is done from Python via copy_expert() (see src/run_pipeline.py),
-- because server-side COPY FROM '<path>' requires the file to exist on the
-- Postgres server's filesystem, not the client's. Keeping this file for
-- reference / manual psql use only:
--
-- \copy raw_customers   FROM 'data/customers.csv'   DELIMITER ',' CSV HEADER;
-- \copy raw_restaurants FROM 'data/restaurants.csv' DELIMITER ',' CSV HEADER;
-- \copy raw_orders      FROM 'data/orders.csv'      DELIMITER ',' CSV HEADER;
