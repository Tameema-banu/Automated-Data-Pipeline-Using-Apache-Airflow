import json
import pandas as pd
from io import StringIO
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# Azure Blob connection
def transform_data():
    try:
        connection_string = "your connection string"  # Replace this
        raw_container = "weather-raw"
        processed_container = "weather-processed"

        # Connect to blob service
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get list of blobs in the raw container
        raw_container_client = blob_service_client.get_container_client(raw_container)
        blobs_list = raw_container_client.list_blobs()

        # Pick the latest blob (assuming by name)
        latest_blob = sorted(blobs_list, key=lambda x: x.name, reverse=True)[0]
        blob_name = latest_blob.name

        print(f"Processing blob: {blob_name}")

        # Download the blob content
        blob_client = raw_container_client.get_blob_client(blob=blob_name)
        blob_data = blob_client.download_blob().readall()
        json_data = json.loads(blob_data)

        # Extract relevant fields from JSON
        processed_data = {
            "city": json_data["name"],
            "timestamp": datetime.utcfromtimestamp(json_data["dt"]),
            "weather": json_data["weather"][0]["description"],
            "temperature": json_data["main"]["temp"] - 273.15,  # Kelvin to Celsius
            "humidity": json_data["main"]["humidity"],
            "wind_speed": json_data["wind"]["speed"]
        }

        # Convert to DataFrame
        df = pd.DataFrame([processed_data])

        # Convert to CSV string
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Upload to weather-processed container
        processed_filename = f"processed_weather_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        processed_blob_client = blob_service_client.get_blob_client(container=processed_container, blob=processed_filename)

        processed_blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

        print(f"Uploaded processed data to {processed_filename}")
    except Exception as e:
        print("Error in transform_data:",e)
    
if __name__ == "__main__":
    transform_data()