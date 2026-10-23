-- Run this once to bootstrap the schema. Safe to re-run (idempotent).

CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id   INTEGER PRIMARY KEY,
    signup_date   DATE NOT NULL,
    city          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_restaurants (
    restaurant_id    INTEGER PRIMARY KEY,
    restaurant_name  TEXT NOT NULL,
    cuisine          TEXT NOT NULL,
    zone             TEXT NOT NULL,
    zone_lat         NUMERIC(9, 6) NOT NULL,
    zone_lng         NUMERIC(9, 6) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_orders (
    order_id                UUID PRIMARY KEY,
    customer_id             INTEGER NOT NULL REFERENCES raw_customers(customer_id),
    restaurant_id           INTEGER NOT NULL REFERENCES raw_restaurants(restaurant_id),
    order_amount             NUMERIC(10, 2) NOT NULL,
    order_timestamp          TIMESTAMP NOT NULL,
    delivery_time_minutes    INTEGER NOT NULL,
    customer_rating_food     NUMERIC(2, 1) NOT NULL
);
