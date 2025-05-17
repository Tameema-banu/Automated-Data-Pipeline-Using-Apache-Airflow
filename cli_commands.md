
# 🛠️ Environment & CLI Setup Guide

This document includes all command-line instructions used to run the Weather ETL Pipeline project using Dockerized Apache Airflow and Azure.

---

## ✨ Install & Setup

### Install WSL (if not already installed)
```bash
wsl --install
```

### Navigate to Project Directory (on D: drive)
```bash
D:
cd path\to\your\airflow-project-folder
```

### Start Docker Desktop (from Start Menu manually)

---

## 🚀 Launch Apache Airflow
```bash
docker-compose up -d
```

---

## 📂 Access Airflow Container

### Enter the webserver container
```bash
docker exec -it docker-airflow_webserver_1 /bin/bash
```

### Navigate to the DAGs folder inside container
```bash
cd /usr/local/airflow/dags
ls
```

### (Optional) Manually test your scripts
```bash
python3 extract.py
python3 transform.py
python3 load.py
```

---

## 🔄 Restart or Relaunch Airflow

### Restart containers
```bash
docker-compose restart
```

### Or bring down and restart
```bash
docker-compose down
docker-compose up -d
```

---

## 📦 Python Package Management (Inside Container)

### Upgrade pip
```bash
pip install --upgrade pip
```

### Install required packages
```bash
pip install azure-storage-blob
pip install pandas
pip install sqlalchemy
```

---

## 🗓️ Airflow CLI Commands (Inside Container)

### Trigger your DAG
```bash
airflow dags trigger weather_etl_pipeline
```

### List available DAGs
```bash
airflow dags list
```

### Check DAG run state
```bash
airflow dags state weather_etl_pipeline <execution_date>
```

### View logs of a specific task
```bash
airflow tasks logs transform_weather_data <execution_date>
```

---

## 📃 Miscellaneous

### Check running Docker containers
```bash
docker ps
```

### View logs of a container
```bash
docker logs docker-airflow_webserver_1
```

### Exit the container
```bash
exit
```

---

> Add this file to your repository as `cli_commands.md` or `run_guide.md`.
