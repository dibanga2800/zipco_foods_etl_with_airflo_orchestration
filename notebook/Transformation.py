import pandas as pd

def run_transformation():
    import os
    csv_path = os.path.join(os.path.dirname(__file__), 'zipco_transaction.csv')
    data = pd.read_csv(csv_path)
    # Remove duplicates
    data.drop_duplicates(inplace=True)

    #Handle missing values (filling missing values with the mean or median of the column)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        data.fillna({col: data[col].mean()}, inplace=True)

    #Handle missing values (fill missing string/object values with 'Unknown')
    string_columns = data.select_dtypes(include=['object']).columns
    for col in string_columns:
        data.fillna({col:'Unknown'}, inplace=True)

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    #Creating dim and fact tables
    #create the product table
    products = data[['ProductName']].drop_duplicates().reset_index(drop=True)
    products.index.name = 'product_id'
    products = products.reset_index()

    #create the staff table
    staff = data[['Staff_Name', 'Staff_Email']].drop_duplicates().reset_index(drop=True)
    staff.index.name = 'staff_id'
    staff = staff.reset_index()

    #create the customer table
    customers = data[['CustomerName', 'CustomerAddress','Customer_PhoneNumber', 'CustomerEmail']].drop_duplicates().reset_index(drop=True)
    customers.index.name = 'customer_id'
    customers = customers.reset_index()

    #Create Transactions tables
    transactions = data.merge(products, on=['ProductName'], how='left') \
                    .merge(staff, on=['Staff_Name', 'Staff_Email'], how='left') \
                    .merge(customers, on=['CustomerName', 'CustomerAddress','Customer_PhoneNumber', 'CustomerEmail'], how='left') \
            
    transactions.index.name = 'transaction_id'
    transactions = transactions.reset_index() \
    [['transaction_id', 'product_id', 'customer_id', 'staff_id', 'Date', 'Quantity', 'UnitPrice', \
        'StoreLocation', 'PaymentType', 'PromotionApplied', 'Weather','Temperature', 'StaffPerformanceRating', 'CustomerFeedback', \
        'DeliveryTime_min', 'OrderType','DayOfWeek', 'TotalSales']]
    
    #Save data to CSV files
    data.to_csv(r'..\dataset\cleaned_data.csv', index=False)   
    products.to_csv(r'..\dataset\products.csv', index=False)
    staff.to_csv(r'..\dataset\staff.csv', index=False)
    customers.to_csv(r'..\dataset\customers.csv', index=False)
    transactions.to_csv(r'..\dataset\transactions.csv', index=False)

    print('Data cleaning and transformation completed successfully.')