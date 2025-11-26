# data/seed_data.py

import os
import sqlite3
import random
import numpy as np

from data import DB_PATH, create_table

BASE_AMT = 3
SCALING_FACTOR = 5

def generate_mock_data():
    users = list(range(1,101))  # User IDs from 1 to 100
    merchants = list(range(1,4)) # Merchant IDs from 1 to 3
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for user_id in users:
        num_visits = max(1, min(3,int(np.random.normal(1.8,0.7))))  # At least 1 visit, average around 1.5
        visited_merchants = random.sample(merchants, np.round(num_visits))
        # calculate total visits per merchant
        for merchant_id in visited_merchants:
            total_visits = int(random.uniform(1,20))  # Between 1 and 20 visits            
            # apply chi square distribution to find money spent per visit
            amount_spent = BASE_AMT + np.random.chisquare(3, size=total_visits) * SCALING_FACTOR            
            for value in amount_spent:
                cursor.execute(
                    "INSERT INTO spendings (user_id, merchant_id, amount) VALUES (?, ?, ?)",
                    (user_id, merchant_id, value)
                )
    
    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Existing database removed.")
        create_table(DB_PATH)
        print("New database and table created.")
    generate_mock_data()
    print("Mock data generated and inserted into the database.")