import os
import random

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

DATA_DIR = os.environ.get("DATA_DIR", "./data")
NUM_CUSTOMERS = 5000
NUM_RESTAURANTS = 500
NUM_ORDERS = 25000

fake = Faker("en_IN")
Faker.seed(None)


def generate_customers() -> pd.DataFrame:
    return pd.DataFrame({
        "customer_id": np.arange(1000, 1000 + NUM_CUSTOMERS),
        "signup_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(NUM_CUSTOMERS)],
        "city": np.random.choice(["Bengaluru", "Mumbai", "Delhi", "Chennai"], NUM_CUSTOMERS),
    })


# Tableau's built-in geocoder doesn't reliably resolve informal Bengaluru
# locality names, so we ship real coordinates for each zone rather than
# relying on text-based auto geocoding in the dashboard.
ZONE_COORDS = {
    "Koramangala": (12.9352, 77.6245),
    "Indiranagar": (12.9784, 77.6408),
    "HSR Layout":  (12.9116, 77.6389),
    "Whitefield":  (12.9698, 77.7500),
    "Jayanagar":   (12.9250, 77.5938),
}


def generate_restaurants() -> pd.DataFrame:
    cuisines = ["North Indian", "South Indian", "Chinese", "Pizza", "Biryani", "Cafe"]
    zones = list(ZONE_COORDS.keys())
    chosen_zones = np.random.choice(zones, NUM_RESTAURANTS)
    return pd.DataFrame({
        "restaurant_id": np.arange(2000, 2000 + NUM_RESTAURANTS),
        "restaurant_name": [fake.company() + " Foods" for _ in range(NUM_RESTAURANTS)],
        "cuisine": np.random.choice(cuisines, NUM_RESTAURANTS),
        "zone": chosen_zones,
        "zone_lat": [ZONE_COORDS[z][0] for z in chosen_zones],
        "zone_lng": [ZONE_COORDS[z][1] for z in chosen_zones],
    })


def generate_orders(customers_df: pd.DataFrame, restaurants_df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "order_id": [fake.uuid4() for _ in range(NUM_ORDERS)],
        "customer_id": np.random.choice(customers_df["customer_id"], NUM_ORDERS),
        "restaurant_id": np.random.choice(restaurants_df["restaurant_id"], NUM_ORDERS),
        "order_amount": np.round(np.random.uniform(150.0, 1200.0, NUM_ORDERS), 2),
        "order_timestamp": [fake.date_time_between(start_date="-1y", end_date="now") for _ in range(NUM_ORDERS)],
        "delivery_time_minutes": np.random.randint(15, 61, NUM_ORDERS),
        "customer_rating_food": np.round(np.random.uniform(1.0, 5.0, NUM_ORDERS), 1),
    })


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    customers_df = generate_customers()
    restaurants_df = generate_restaurants()
    orders_df = generate_orders(customers_df, restaurants_df)

    customers_df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
    restaurants_df.to_csv(os.path.join(DATA_DIR, "restaurants.csv"), index=False)
    orders_df.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)

    print(f"Synthetic data generated in '{DATA_DIR}': "
          f"{len(customers_df)} customers, {len(restaurants_df)} restaurants, {len(orders_df)} orders.")


if __name__ == "__main__":
    main()
