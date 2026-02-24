"""
Dataset Download Script
Taobao Maternity Shopping Dataset - Requires manual login
"""
import os
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_RAW = PROJECT_DIR / "data" / "raw"

# Ensure directory exists
DATA_RAW.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Taobao Maternity Shopping Dataset Download")
print("=" * 60)
print(f"\nData will be saved to: {DATA_RAW}")
print("\n[!] Note: Tianchi dataset requires login to download")
print("\n[Manual Download Steps]:")
print("1. Visit: https://tianchi.aliyun.com/dataset/45")
print("2. Login with Alibaba Cloud account")
print("3. Click 'Download Dataset'")
print("4. Place downloaded files in:")
print(f"   {DATA_RAW}")
print("\n[Required Files]:")
print("   - (sample)sam_tianchi_mum_baby.csv")
print("   - (sample)sam_tianchi_mum_baby_trade_history.csv")
print("\n[!] Note: Prefix (sample)sam_ indicates sample data")
print("=" * 60)

# Check for existing data files
existing_files = list(DATA_RAW.glob("*.csv"))
if existing_files:
    print(f"\n[OK] Found {len(existing_files)} CSV file(s):")
    for f in existing_files:
        print(f"   - {f.name}")
else:
    print("\n[WAIT] No data files found. Please download manually first.")
