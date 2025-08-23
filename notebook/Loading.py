import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

#Data Loading
def run_loading():
    #Loading the dataset
    data = pd.read_csv(r'..\dataset\cleaned_data.csv')
    products = pd.read_csv(r'..\dataset\products.csv')
    staff = pd.read_csv(r'..\dataset\staff.csv')
    customers = pd.read_csv(r'..\dataset\customers.csv')
    transactions = pd.read_csv(r'..\dataset\transactions.csv')

    #Load the enviroment variables from the .env files
    load_dotenv()

    connect_str = os.getenv("AZURE_CONNECTION_STRING_VALUE")
    container_name = os.getenv("CONTAINER_NAME")

    #Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)

    #Load data to Azure Blob Storage
    files = [
        (data, 'rawdata/cleaned_zipco_transaction_data.csv'),
        (products, 'cleaneddata/products.csv'),
        (staff, 'cleaneddata/staff.csv'),
        (customers, 'cleaneddata/customers.csv'),
        (transactions, 'cleaneddata/transactions.csv')
    ]

    for file, blob_name in files:
        blob_client = container_client.get_blob_client(blob_name)
        output = file.to_csv(index=False)
        blob_client.upload_blob(output, overwrite=True)
        print(f"Uploaded {blob_name} to Azure Blob Storage successfully.")