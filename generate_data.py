import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

# Initialize Faker for Indian data
fake = Faker('en_IN')

# Define how many records to create
NUM_CUSTOMERS = 5000
NUM_RESTAURANTS = 500
NUM_ORDERS = 25000

# --- Generate Customers ---
customers = []
for i in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': 1000 + i,
        'signup_date': fake.date_between(start_date='-2y', end_date='today'),
        'city': random.choice(['Bengaluru', 'Mumbai', 'Delhi', 'Chennai'])
    })
customers_df = pd.DataFrame(customers)

# --- Generate Restaurants ---
restaurants = []
cuisines = ['North Indian', 'South Indian', 'Chinese', 'Pizza', 'Biryani', 'Cafe']
for i in range(NUM_RESTAURANTS):
    restaurants.append({
        'restaurant_id': 2000 + i,
        'restaurant_name': fake.company() + " Foods",
        'cuisine': random.choice(cuisines),
        'zone': random.choice(['Koramangala', 'Indiranagar', 'HSR Layout', 'Whitefield', 'Jayanagar'])
    })
restaurants_df = pd.DataFrame(restaurants)

# --- Generate Orders ---
orders = []
for _ in range(NUM_ORDERS):
    orders.append({
        'order_id': fake.uuid4(),
        'customer_id': random.choice(customers_df['customer_id']),
        'restaurant_id': random.choice(restaurants_df['restaurant_id']),
        'order_amount': round(random.uniform(150.0, 1200.0), 2),
        'order_timestamp': fake.date_time_between(start_date='-1y', end_date='now'),
        'delivery_time_minutes': random.randint(15, 60),
        'customer_rating_food': round(random.uniform(1.0, 5.0), 1)
    })
orders_df = pd.DataFrame(orders)

# Save the dataframes to CSV files in the 'data' folder
# Save to CSV
customers_df.to_csv('C:/New folder/data/customers.csv', index=False)
restaurants_df.to_csv('C:/New folder/data/restaurants.csv', index=False)
orders_df.to_csv('C:/New folder/data/orders.csv', index=False)
print("✅ Synthetic data generated successfully in the 'data' folder!")