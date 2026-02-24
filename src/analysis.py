"""
Taobao Maternity Shopping Data Analysis
Complete analysis pipeline
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup matplotlib for Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Set style
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8-darkgrid')

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_RAW = PROJECT_DIR / "data" / "raw"
DATA_PROCESSED = PROJECT_DIR / "data" / "processed"
DATA_OUTPUT = PROJECT_DIR / "data" / "output"

# Create directories
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
DATA_OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Taobao Maternity Shopping Data Analysis")
print("=" * 70)

# ============================================
# Phase 1: Data Loading & Cleaning
# ============================================
print("\n[Phase 1/4] Data Loading & Cleaning")
print("-" * 70)

# Load data
print("Loading raw data...")
baby_df = pd.read_csv(DATA_RAW / "tianchi_mum_baby.csv")
trade_df = pd.read_csv(DATA_RAW / "tianchi_mum_baby_trade_history.csv")

print(f"  Baby info: {len(baby_df):,} records")
print(f"  Trade history: {len(trade_df):,} records")

# Clean baby data
print("\nCleaning baby data...")
baby_df['birthday'] = pd.to_datetime(baby_df['birthday'], format='%Y%m%d')
baby_df['gender_label'] = baby_df['gender'].map({0: 'Female', 1: 'Male', 2: 'Unknown'})
print(f"  Date range: {baby_df['birthday'].min()} to {baby_df['birthday'].max()}")

# Clean trade data
print("\nCleaning trade data...")
trade_df['day'] = pd.to_datetime(trade_df['day'], format='%Y%m%d')
trade_df['year'] = trade_df['day'].dt.year
trade_df['month'] = trade_df['day'].dt.month
trade_df['year_month'] = trade_df['day'].dt.to_period('M')
print(f"  Date range: {trade_df['day'].min()} to {trade_df['day'].max()}")

# Check for outliers in buy_mount
print("\nChecking for outliers...")
q99 = trade_df['buy_mount'].quantile(0.99)
outliers = trade_df[trade_df['buy_mount'] > q99]
print(f"  99th percentile: {q99}")
print(f"  Outliers (>99th percentile): {len(outliers)} records")

# Remove extreme outliers (likely data errors)
trade_clean = trade_df[trade_df['buy_mount'] <= 100].copy()
print(f"  Records after cleaning: {len(trade_clean):,}")

# Merge datasets
print("\nMerging datasets...")
merged_df = trade_clean.merge(baby_df, on='user_id', how='left')
merged_df['baby_age_days'] = (merged_df['day'] - merged_df['birthday']).dt.days
merged_df['baby_age_months'] = (merged_df['baby_age_days'] / 30).astype(int)
print(f"  Merged records: {len(merged_df):,}")

# Save processed data
merged_df.to_csv(DATA_PROCESSED / "merged_data.csv", index=False)
baby_df.to_csv(DATA_PROCESSED / "baby_clean.csv", index=False)
trade_clean.to_csv(DATA_PROCESSED / "trade_clean.csv", index=False)
print(f"\nSaved processed data to: {DATA_PROCESSED}")

# ============================================
# Phase 2: User Profile Analysis
# ============================================
print("\n[Phase 2/4] User Profile Analysis")
print("-" * 70)

# Gender distribution
print("\nAnalyzing gender distribution...")
gender_dist = baby_df['gender_label'].value_counts()
print(gender_dist)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gender pie chart
colors = ['#FF9999', '#66B2FF', '#99FF99']
axes[0].pie(gender_dist.values, labels=gender_dist.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
axes[0].set_title('Baby Gender Distribution', fontsize=14, fontweight='bold')

# Baby age distribution at time of purchase
baby_age_purchases = merged_df[merged_df['baby_age_months'] >= 0]['baby_age_months']
axes[1].hist(baby_age_purchases, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Baby Age (Months)')
axes[1].set_ylabel('Number of Purchases')
axes[1].set_title('Purchase Distribution by Baby Age', fontsize=14, fontweight='bold')
axes[1].axvline(baby_age_purchases.median(), color='red', linestyle='--', 
                label=f'Median: {baby_age_purchases.median():.1f} months')
axes[1].legend()

plt.tight_layout()
plt.savefig(DATA_OUTPUT / "user_profile_analysis.png", dpi=150, bbox_inches='tight')
print(f"  Saved: user_profile_analysis.png")
plt.close()

# Age group analysis
print("\nAnalyzing age groups...")
age_bins = [0, 6, 12, 24, 36, 72]
age_labels = ['0-6m', '6-12m', '1-2y', '2-3y', '3y+']
merged_df['age_group'] = pd.cut(merged_df['baby_age_months'], bins=age_bins, 
                                 labels=age_labels, right=False)
age_group_stats = merged_df.groupby('age_group').agg({
    'buy_mount': ['count', 'sum', 'mean'],
    'user_id': 'nunique'
}).round(2)
print(age_group_stats)

# ============================================
# Phase 3: Product Analysis
# ============================================
print("\n[Phase 3/4] Product Analysis")
print("-" * 70)

# Category analysis
print("\nAnalyzing product categories...")
category_stats = merged_df.groupby('category').agg({
    'buy_mount': ['count', 'sum'],
    'user_id': 'nunique'
}).round(2)
category_stats.columns = ['purchase_count', 'total_quantity', 'unique_users']
category_stats = category_stats.sort_values('purchase_count', ascending=False)
print(category_stats.head(10))

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top categories by purchase count
top_categories = category_stats.head(10)
axes[0, 0].barh(range(len(top_categories)), top_categories['purchase_count'], color='steelblue')
axes[0, 0].set_yticks(range(len(top_categories)))
axes[0, 0].set_yticklabels(top_categories.index)
axes[0, 0].set_xlabel('Purchase Count')
axes[0, 0].set_title('Top 10 Categories by Purchase Count', fontsize=12, fontweight='bold')
axes[0, 0].invert_yaxis()

# Category by quantity sold
axes[0, 1].barh(range(len(top_categories)), top_categories['total_quantity'], color='coral')
axes[0, 1].set_yticks(range(len(top_categories)))
axes[0, 1].set_yticklabels(top_categories.index)
axes[0, 1].set_xlabel('Total Quantity Sold')
axes[0, 1].set_title('Top 10 Categories by Quantity', fontsize=12, fontweight='bold')
axes[0, 1].invert_yaxis()

# Purchase quantity distribution
axes[1, 0].hist(merged_df['buy_mount'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Purchase Quantity')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Distribution of Purchase Quantities', fontsize=12, fontweight='bold')

# Top products
print("\nTop 20 products by purchase count...")
top_products = merged_df.groupby('auction_id').agg({
    'buy_mount': ['count', 'sum'],
    'user_id': 'nunique'
}).round(2)
top_products.columns = ['purchase_count', 'total_quantity', 'unique_users']
top_products = top_products.sort_values('purchase_count', ascending=False).head(20)

axes[1, 1].barh(range(len(top_products)), top_products['purchase_count'], color='mediumpurple')
axes[1, 1].set_yticks(range(len(top_products)))
axes[1, 1].set_yticklabels([f"Product {i+1}" for i in range(len(top_products))], fontsize=8)
axes[1, 1].set_xlabel('Purchase Count')
axes[1, 1].set_title('Top 20 Products', fontsize=12, fontweight='bold')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig(DATA_OUTPUT / "product_analysis.png", dpi=150, bbox_inches='tight')
print(f"  Saved: product_analysis.png")
plt.close()

# ============================================
# Phase 4: Time Trend Analysis
# ============================================
print("\n[Phase 4/4] Time Trend Analysis")
print("-" * 70)

# Monthly trend
print("\nAnalyzing monthly trends...")
monthly_sales = merged_df.groupby('year_month').agg({
    'buy_mount': ['count', 'sum'],
    'user_id': 'nunique'
}).reset_index()
monthly_sales.columns = ['year_month', 'purchase_count', 'total_quantity', 'unique_users']

fig, axes = plt.subplots(3, 1, figsize=(16, 12))

# Purchase count trend
axes[0].plot(range(len(monthly_sales)), monthly_sales['purchase_count'], 
             marker='o', linewidth=2, markersize=4, color='steelblue')
axes[0].set_ylabel('Purchase Count')
axes[0].set_title('Monthly Purchase Count Trend', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Quantity trend
axes[1].plot(range(len(monthly_sales)), monthly_sales['total_quantity'], 
             marker='s', linewidth=2, markersize=4, color='coral')
axes[1].set_ylabel('Total Quantity')
axes[1].set_title('Monthly Total Quantity Trend', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

# Unique users trend
axes[2].plot(range(len(monthly_sales)), monthly_sales['unique_users'], 
             marker='^', linewidth=2, markersize=4, color='green')
axes[2].set_ylabel('Unique Users')
axes[2].set_xlabel('Time Period')
axes[2].set_title('Monthly Unique Users Trend', fontsize=12, fontweight='bold')
axes[2].grid(True, alpha=0.3)

# Set x-axis labels (every 6 months)
tick_positions = range(0, len(monthly_sales), 6)
tick_labels = [str(monthly_sales.iloc[i]['year_month']) for i in tick_positions]
for ax in axes:
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

plt.tight_layout()
plt.savefig(DATA_OUTPUT / "time_trend_analysis.png", dpi=150, bbox_inches='tight')
print(f"  Saved: time_trend_analysis.png")
plt.close()

# Year-over-year comparison
print("\nYear-over-year analysis...")
yearly_stats = merged_df.groupby('year').agg({
    'buy_mount': ['count', 'sum'],
    'user_id': 'nunique'
}).round(2)
yearly_stats.columns = ['purchase_count', 'total_quantity', 'unique_users']
print(yearly_stats)

# ============================================
# Phase 5: RFM Analysis
# ============================================
print("\n[Bonus] RFM Customer Value Analysis")
print("-" * 70)

# Calculate RFM metrics
reference_date = merged_df['day'].max() + timedelta(days=1)
print(f"\nReference date: {reference_date.date()}")

rfm = merged_df.groupby('user_id').agg({
    'day': lambda x: (reference_date - x.max()).days,  # Recency
    'auction_id': 'count',  # Frequency
    'buy_mount': 'sum'  # Monetary
}).reset_index()
rfm.columns = ['user_id', 'recency', 'frequency', 'monetary']

print(f"\nRFM metrics calculated for {len(rfm)} users")
print(rfm.describe())

# RFM scoring (1-5 scale)
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])  # Lower recency = higher score
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

# Convert to numeric
rfm['r_score'] = rfm['r_score'].astype(int)
rfm['f_score'] = rfm['f_score'].astype(int)
rfm['m_score'] = rfm['m_score'].astype(int)

# RFM segment
rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

# Simple segmentation
def segment_customer(row):
    if row['r_score'] >= 4 and row['f_score'] >= 4 and row['m_score'] >= 4:
        return 'Champions'
    elif row['r_score'] >= 3 and row['f_score'] >= 3 and row['m_score'] >= 3:
        return 'Loyal Customers'
    elif row['r_score'] >= 4 and row['f_score'] <= 2:
        return 'New Customers'
    elif row['r_score'] <= 2 and row['f_score'] >= 3:
        return 'At Risk'
    elif row['r_score'] <= 2 and row['f_score'] <= 2 and row['m_score'] >= 3:
        return 'Cannot Lose Them'
    else:
        return 'Others'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

# Segment distribution
print("\nCustomer Segments:")
segment_dist = rfm['segment'].value_counts()
print(segment_dist)

# Save RFM results
rfm.to_csv(DATA_PROCESSED / "rfm_analysis.csv", index=False)
print(f"\nSaved RFM analysis to: {DATA_PROCESSED / 'rfm_analysis.csv'}")

# Visualize RFM
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# RFM distributions
axes[0, 0].hist(rfm['recency'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Recency (Days)')
axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title('Recency Distribution', fontweight='bold')

axes[0, 1].hist(rfm['frequency'], bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Frequency (Purchases)')
axes[0, 1].set_ylabel('Count')
axes[0, 1].set_title('Frequency Distribution', fontweight='bold')

axes[1, 0].hist(rfm['monetary'], bins=30, color='coral', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Monetary (Quantity)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Monetary Distribution', fontweight='bold')

# Segment distribution
segment_colors = plt.cm.Set3(range(len(segment_dist)))
axes[1, 1].pie(segment_dist.values, labels=segment_dist.index, autopct='%1.1f%%',
               colors=segment_colors, startangle=90)
axes[1, 1].set_title('Customer Segment Distribution', fontweight='bold')

plt.tight_layout()
plt.savefig(DATA_OUTPUT / "rfm_analysis.png", dpi=150, bbox_inches='tight')
print(f"  Saved: rfm_analysis.png")
plt.close()

# ============================================
# Summary Report
# ============================================
print("\n" + "=" * 70)
print("Analysis Complete!")
print("=" * 70)

print("\n[Key Findings]:")
print(f"  - Total users: {baby_df['user_id'].nunique():,}")
print(f"  - Total transactions: {len(trade_clean):,}")
print(f"  - Total quantity sold: {trade_clean['buy_mount'].sum():,}")
print(f"  - Average purchase quantity: {trade_clean['buy_mount'].mean():.2f}")
print(f"  - Date range: {trade_clean['day'].min().date()} to {trade_clean['day'].max().date()}")

print(f"\n[Top Category]: {category_stats.index[0]} ({category_stats.iloc[0]['purchase_count']} purchases)")
print(f"[Champions]: {segment_dist.get('Champions', 0)} customers ({segment_dist.get('Champions', 0)/len(rfm)*100:.1f}%)")

print("\n[Output Files]:")
print(f"  Processed data: {DATA_PROCESSED}")
print(f"  Visualizations: {DATA_OUTPUT}")
for f in DATA_OUTPUT.glob("*.png"):
    print(f"    - {f.name}")

print("\n" + "=" * 70)
