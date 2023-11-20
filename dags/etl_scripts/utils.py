import os
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError
from io import StringIO

def load_object(data,file):
    account_name = os.getenv("account_name")
    account_key = os.getenv("account_key")
    container_name = os.getenv("container_name")
    upload_to_cloud(account_name,account_key,container_name, file, data)

def get_object(file):
    account_name = os.getenv("account_name")
    account_key = os.getenv("account_key")
    container_name = os.getenv("container_name")
    df = get_from_cloud(account_name,account_key,container_name,file)
    return df


def upload_to_cloud(account_name, account_key, container_name, file_name, data):
    # Create a connection to the Azure Storage account
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()

    # Upload data to a file in the container
    blob_client = container_client.get_blob_client(file_name)
    data = data.to_csv(index=False)
    blob_client.upload_blob(data)


def get_from_cloud(account_name,account_key,container_name,file):
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    container_client = blob_service_client.get_container_client(container_name)
    try:
        blob_client = container_client.get_blob_client(file)

        content = blob_client.download_blob().readall()

        df = pd.read_csv(StringIO(content.decode('utf-8')))
    
    except ResourceNotFoundError:
        df = pd.DataFrame()
    
    return df








