import pandas as pd

def generate_analytics(df: pd.DataFrame) -> dict:
    """Generate analytics reports from order data"""
    
    # Calculate profit (List Price - Cost Price) * Quantity * (1 - Discount Percent/100)
    df['profit'] = (df['List Price'] - df['cost price']) * df['Quantity'] * (1 - df['Discount Percent']/100)
    
    # 1. Most profitable region
    region_profit = df.groupby('Region')['profit'].sum().reset_index()
    region_profit = region_profit.sort_values('profit', ascending=False)
    
    # 2. Most common shipping method for each product category
    shipping_by_category = df.groupby(['Category', 'Ship Mode']).size().reset_index(name='count')
    most_common_shipping = shipping_by_category.loc[shipping_by_category.groupby('Category')['count'].idxmax()]
    most_common_shipping = most_common_shipping[['Category', 'Ship Mode', 'count']].reset_index(drop=True)
    
    # 3. Number of orders by category and sub-category
    orders_by_category = df.groupby(['Category', 'Sub Category']).size().reset_index(name='order_count')
    
    return {
        'most_profitable_region': region_profit,
        'shipping_method_by_category': most_common_shipping,
        'orders_by_category_subcategory': orders_by_category
    }

def calculate_profit_by_order(orders_df):
    """Calculate profit for each order in the DataFrame"""
    orders_df['profit'] = (orders_df['List Price'] - orders_df['cost price']) * orders_df['Quantity'] * (1 - orders_df['Discount Percent']/100)
    return orders_df

def calculate_most_profitable_region(orders_df):
    """Calculate the most profitable region and its profit"""
    orders_df = calculate_profit_by_order(orders_df)
    return orders_df.groupby('Region')['profit'].sum().reset_index().sort_values('profit', ascending=False)

def find_most_common_ship_method(orders_df):
    """Find the most common shipping method for each Category"""
    shipping_by_category = orders_df.groupby(['Category', 'Ship Mode']).size().reset_index(name='count')
    return shipping_by_category.loc[shipping_by_category.groupby('Category')['count'].idxmax()].reset_index(drop=True)

def find_number_of_order_per_category(orders_df):
    """Find the number of orders for each Category and Sub Category"""
    return orders_df.groupby(['Category', 'Sub Category']).size().reset_index(name='order_count')