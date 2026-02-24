"""
Generate Sample Data for Taobao Maternity Shopping Analysis
This creates simulated data matching the structure of the real dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_RAW = PROJECT_DIR / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Generating Sample Data")
print("=" * 60)

# ============================================
# Table 1: Baby Information
# ============================================
print("\n[1/2] Generating baby info table...")

n_users = 1000
user_ids = [f"user_{i:05d}" for i in range(1, n_users + 1)]

# Generate birthdays (2010-2014)
start_date = datetime(2010, 1, 1)
end_date = datetime(2014, 12, 31)
date_range = (end_date - start_date).days

birthdays = []
for _ in range(n_users):
    random_days = random.randint(0, date_range)
    birthday = start_date + timedelta(days=random_days)
    birthdays.append(birthday.strftime("%Y%m%d"))

# Gender: 0=female, 1=male, 2=unknown
genders = np.random.choice([0, 1, 2], size=n_users, p=[0.45, 0.45, 0.10])

baby_df = pd.DataFrame({
    "user_id": user_ids,
    "birthday": birthdays,
    "gender": genders
})

# Save baby info
baby_file = DATA_RAW / "tianchi_mum_baby.csv"
baby_df.to_csv(baby_file, index=False)
print(f"   Saved: {baby_file.name} ({len(baby_df)} records)")

# ============================================
# Table 2: Trade History
# ============================================
print("\n[2/2] Generating trade history table...")

# Generate transactions
n_transactions = 15000

# Select random users (with some users having multiple transactions)
user_samples = np.random.choice(user_ids, size=n_transactions)

# Generate auction IDs
auction_ids = [f"auction_{i:08d}" for i in range(1, n_transactions + 1)]

# Categories
main_categories = [28, 38, 50008168, 50014815, 50022520]
categories = np.random.choice(main_categories, size=n_transactions)

# Sub-categories (500+ unique)
sub_categories = [random.randint(10000000, 99999999) for _ in range(n_transactions)]

# Properties (simplified)
properties = [f"property_{random.randint(1, 100)}" for _ in range(n_transactions)]

# Purchase amounts (buy_mount) - mostly 1-5, some larger
buy_mounts = np.random.choice(
    [1, 1, 1, 2, 2, 3, 3, 4, 5, random.randint(6, 20)],
    size=n_transactions
)

# Day (2012-2015)
trade_start = datetime(2012, 1, 1)
trade_end = datetime(2015, 12, 31)
trade_range = (trade_end - trade_start).days

days = []
for _ in range(n_transactions):
    random_days = random.randint(0, trade_range)
    trade_day = trade_start + timedelta(days=random_days)
    days.append(int(trade_day.strftime("%Y%m%d")))

trade_df = pd.DataFrame({
    "user_id": user_samples,
    "auction_id": auction_ids,
    "category": categories,
    "cat": sub_categories,
    "property": properties,
    "buy_mount": buy_mounts,
    "day": days
})

# Save trade history
trade_file = DATA_RAW / "tianchi_mum_baby_trade_history.csv"
trade_df.to_csv(trade_file, index=False)
print(f"   Saved: {trade_file.name} ({len(trade_df)} records)")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 60)
print("Sample Data Generated Successfully!")
print("=" * 60)
print(f"\n[Files Created]:")
print(f"   1. {baby_file.name}")
print(f"      - Records: {len(baby_df)}")
print(f"      - Columns: {list(baby_df.columns)}")
print(f"\n   2. {trade_file.name}")
print(f"      - Records: {len(trade_df)}")
print(f"      - Columns: {list(trade_df.columns)}")
print(f"\n[Location]: {DATA_RAW}")
print("\n[!] Note: This is simulated data for demonstration.")
print("    Replace with real data from Tianchi when available.")
print("=" * 60)
