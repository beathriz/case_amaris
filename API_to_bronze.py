from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_to_bronze',
    default_args=default_args,
    description='Fetch data from API and save to Bronze layer',
    schedule_interval='@daily',  # Roda diariamente
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

def api_to_bronze():
    api_url = "https://api.openbrewerydb.org/breweries"
    bronze_path = "/data/bronze"
    os.makedirs(bronze_path, exist_ok=True)

    file_name = f"breweries_{datetime.now().strftime('%Y%m%d')}.json"
    file_path = os.path.join(bronze_path, file_name)

    if os.path.exists(file_path):
        print(f"Arquivo já existe: {file_path}. Não será salvo novamente.")
        return

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Dados salvos em: {file_path}")
    else:
        raise Exception(f"Erro ao buscar dados da API. Status code: {response.status_code}")

save_to_volum = PythonOperator(
    task_id='api_to_bronze',
    python_callable=api_to_bronze,
    dag=dag,
)

save_to_volum
