import pandas as pd
import logging

def generate_analytics(df: pd.DataFrame) -> dict:
    """Generate analytics reports from order data with validation"""
    
    # Validate input
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    required_columns = ['List Price', 'cost price', 'Quantity', 'Discount Percent', 'Region', 'Category', 'Ship Mode', 'Sub Category']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Calculate profit with error handling
    try:
        df = df.copy()  # Avoid modifying original DataFrame
        df['profit'] = (df['List Price'] - df['cost price']) * df['Quantity'] * (1 - df['Discount Percent']/100)
    except Exception as e:
        raise ValueError(f"Error calculating profit: {e}")
    
    # 1. Most profitable region
    region_profit = df.groupby('Region')['profit'].sum().reset_index()
    region_profit = region_profit.sort_values('profit', ascending=False)
    
    # 2. Most common shipping method for each product category
    shipping_counts = df.groupby(['Category', 'Ship Mode']).size().reset_index(name='count')
    most_common_shipping = shipping_counts.loc[shipping_counts.groupby('Category')['count'].idxmax()]
    most_common_shipping = most_common_shipping[['Category', 'Ship Mode', 'count']].reset_index(drop=True)
    
    # 3. Number of orders by category and sub-category
    orders_by_category = df.groupby(['Category', 'Sub Category']).size().reset_index(name='order_count')
    
    logging.info(f"Analytics generated for {len(df)} orders")
    
    return {
        'most_profitable_region': region_profit,
        'shipping_method_by_category': most_common_shipping,
        'orders_by_category_subcategory': orders_by_category
    }