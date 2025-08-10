import pandas as pd

#Data Extraction
def run_extraction():
    try:
        data = pd.read_csv(r'..\dataset\zipco_transaction.csv')
        print("Data Extracted successfully.")
    except Exception as e:
        print(f"Error extracting data: {e}")