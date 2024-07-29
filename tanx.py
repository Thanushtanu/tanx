import pandas as pd
from datetime import datetime

def read_data(file_path):
    """
    Reads data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the CSV data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        print("The file is empty. Please provide a valid CSV file.")
        return None
    except pd.errors.ParserError:
        print("Error parsing the file. Please ensure the file is a valid CSV.")
        return None

def compute_monthly_revenue(data):
    """
    Computes the total revenue for each month.

    Parameters:
    data (pd.DataFrame): DataFrame containing the order data.

    Returns:
    pd.Series: Series with the total revenue for each month.
    """
    try:
        data['order_date'] = pd.to_datetime(data['order_date'], errors='coerce')
        data.dropna(subset=['order_date'], inplace=True)
        data['month_year'] = data['order_date'].dt.to_period('M')
        monthly_revenue = data.groupby('month_year').apply(lambda x: (x['product_price'] * x['quantity']).sum())
        return monthly_revenue
    except Exception as e:
        print(f"An error occurred while computing monthly revenue: {e}")
        return pd.Series()

def compute_product_revenue(data):
    """
    Computes the total revenue for each product.

    Parameters:
    data (pd.DataFrame): DataFrame containing the order data.

    Returns:
    pd.Series: Series with the total revenue for each product.
    """
    try:
        product_revenue = data.groupby('product_id').apply(lambda x: (x['product_price'] * x['quantity']).sum())
        return product_revenue
    except Exception as e:
        print(f"An error occurred while computing product revenue: {e}")
        return pd.Series()

def compute_customer_revenue(data):
    """
    Computes the total revenue for each customer.

    Parameters:
    data (pd.DataFrame): DataFrame containing the order data.

    Returns:
    pd.Series: Series with the total revenue for each customer.
    """
    try:
        customer_revenue = data.groupby('customer_id').apply(lambda x: (x['product_price'] * x['quantity']).sum())
        return customer_revenue
    except Exception as e:
        print(f"An error occurred while computing customer revenue: {e}")
        return pd.Series()

def top_10_customers(data):
    """
    Identifies the top 10 customers by revenue.

    Parameters:
    data (pd.DataFrame): DataFrame containing the order data.

    Returns:
    pd.Series: Series with the top 10 customers and their total revenue.
    """
    try:
        customer_revenue = compute_customer_revenue(data)
        top_customers = customer_revenue.sort_values(ascending=False).head(10)
        return top_customers
    except Exception as e:
        print(f"An error occurred while identifying top customers: {e}")
        return pd.Series()

def main(file_path):
    """
    Main function to compute and print the results.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    # Read data from the CSV file
    data = read_data(file_path)
    if data is None or data.empty:
        print("No data available to process.")
        return

    # Calculate and print monthly revenue
    print("Monthly Revenue:")
    monthly_revenue = compute_monthly_revenue(data)
    if not monthly_revenue.empty:
        print(monthly_revenue)
    else:
        print("No data available to calculate monthly revenue.")

    # Calculate and print product revenue
    print("\nProduct Revenue:")
    product_revenue = compute_product_revenue(data)
    if not product_revenue.empty:
        print(product_revenue)
    else:
        print("No data available to calculate product revenue.")

    # Calculate and print customer revenue
    print("\nCustomer Revenue:")
    customer_revenue = compute_customer_revenue(data)
    if not customer_revenue.empty:
        print(customer_revenue)
    else:
        print("No data available to calculate customer revenue.")

    # Calculate and print top 10 customers by revenue
    print("\nTop 10 Customers by Revenue:")
    top_customers = top_10_customers(data)
    if not top_customers.empty:
        print(top_customers)
    else:
        print("No data available to identify top customers.")

# Example usage
if __name__ == "__main__":
    # Replace 'orders.csv' with the path to your CSV file
    main("D:/order.csv")
