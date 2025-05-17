import requests
import json
from azure.storage.blob import BlobServiceClient
from datetime import datetime

def extract_and_upload():
    try:
        city = "Hyderabad"
        api_key = "your api key"  # Replace this
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        print("Requesting weather data...")
        response = requests.get(url)
        print("Response status:", response.status_code)

        if response.status_code != 200:
            print("Failed to fetch data:", response.text)
            return

        data = response.json()
        print("Weather data fetched successfully.")

        filename = f"{city}weather{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

        connection_string = "your connection string"  # Replace this
        container_name = "weather-raw"

        print("Connecting to Azure Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        print(f"Uploading {filename} to Blob Storage...")
        blob_client.upload_blob(json.dumps(data), overwrite=True)
        print("Upload complete.")

    except Exception as e:
        print("Error:", e)

# Call the function
extract_and_upload()