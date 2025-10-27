import pandas as pd
import sys
sys.path.append('./app')
import orders_analytics

# Load sample data
df = pd.read_csv('sample_orders.csv')
print("Sample data loaded:")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\nFirst few rows:")
print(df.head(3))

# Test analytics
analytics = orders_analytics.generate_analytics(df)

print("\n=== ANALYTICS RESULTS ===")

print("\n1. Most Profitable Region:")
print(analytics['most_profitable_region'])

print("\n2. Shipping Method by Category:")
print(analytics['shipping_method_by_category'])

print("\n3. Orders by Category/Sub-Category:")
print(analytics['orders_by_category_subcategory'])

# Manual verification of profit calculation for first row
print("\n=== MANUAL VERIFICATION ===")
first_row = df.iloc[0]
manual_profit = (first_row['List Price'] - first_row['cost price']) * first_row['Quantity'] * (1 - first_row['Discount Percent']/100)
print(f"First row manual profit: {manual_profit}")
print(f"Formula: ({first_row['List Price']} - {first_row['cost price']}) * {first_row['Quantity']} * (1 - {first_row['Discount Percent']}/100)")