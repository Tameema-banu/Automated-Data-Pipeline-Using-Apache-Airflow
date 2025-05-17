from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# Let Airflow access your scripts
sys.path.append("/usr/local/airflow/dags")

# Import your Python scripts
from extract import extract_and_upload
from transform import transform_data
from load import load_data_to_azure_sql

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    description='Extract and transform weather data, upload to Azure Blob',
    schedule_interval='@daily',  # or '@hourly'
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract_weather_data',
    python_callable=extract_and_upload,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_data,
    dag=dag
)
load_task = PythonOperator(
    task_id = 'load_data_to_azure_sql',
    python_callable = load_data_to_azure_sql,
    dag=dag
)


extract_task >> transform_task >> load_task  # set task order




