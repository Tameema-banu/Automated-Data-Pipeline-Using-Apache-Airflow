import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import StringIO
from sqlalchemy import create_engine

def load_data_to_azure_sql():
    try:
        # Azure Blob connection string and container with processed data
        connection_string = "your connection string"
        processed_container = "weather-processed"
        
        # Azure SQL Database credentials
        server = 'airflow-sql-server.database.windows.net'
        database = 'weatherdb'
        username = 'tameema'
        password = 'your password'
        table_name = 'weather_data'
        
        # Create the connection URL (replace with your actual values)
        connection_url = f"mssql+pytds://{username}:{password}@{server}:1433/{database}"

        # Connect to Blob and get latest processed file
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(processed_container)
        blobs_list = container_client.list_blobs()
        latest_blob = sorted(blobs_list, key=lambda x: x.name, reverse=True)[0]

        blob_client = container_client.get_blob_client(latest_blob.name)
        blob_data = blob_client.download_blob().readall()

        df = pd.read_csv(StringIO(blob_data.decode('utf-8')))

        # Use SQLAlchemy to load data
        engine = create_engine(connection_url)
        df.to_sql(table_name, engine, if_exists='append', index=False)

        print("✅ Data loaded to Azure SQL successfully.")

    except Exception as e:
        print("❌ Error loading data to Azure SQL:", e)