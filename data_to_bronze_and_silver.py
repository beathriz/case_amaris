from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os
import json
from pyspark.sql import SparkSession

# Configuração do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_to_bronze_and_silver',
    default_args=default_args,
    description='Fetch data from API and transform to Silver layer',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

def api_to_bronze():
    api_url = "https://api.openbrewerydb.org/breweries"
    bronze_path = "/data/bronze"
    os.makedirs(bronze_path, exist_ok=True)

    file_name = f"breweries_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
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

def transform_to_silver():
    bronze_path = "/data/bronze"
    silver_path = "/data/silver"
    os.makedirs(silver_path, exist_ok=True)

    spark = SparkSession.builder \
        .appName("Transform to Silver") \
        .getOrCreate()

    # Carregar arquivos JSON da Camada Bronze
    json_files = [os.path.join(bronze_path, f) for f in os.listdir(bronze_path) if f.endswith('.json')]

    if not json_files:
        raise Exception("Nenhum arquivo JSON encontrado na camada Bronze.")

    for file in json_files:
        print(f"Processando o arquivo: {file}")
        df = spark.read.option("multiline", "true").json(file)

        # Validar o schema do DataFrame
        if 'state' not in df.columns:
            print(f"O arquivo {file} está corrompido ou faltando o campo 'state'.")
            continue

        # Transformar e salvar em parquet, particionado por localização (estado)
        df.write.partitionBy("state").mode("append").parquet(silver_path)

    print(f"Dados transformados e salvos na camada Silver em: {silver_path}")

save_to_bronze = PythonOperator(
    task_id='api_to_bronze',
    python_callable=api_to_bronze,
    dag=dag,
)

save_to_silver = PythonOperator(
    task_id='transform_to_silver',
    python_callable=transform_to_silver,
    dag=dag,
)

save_to_bronze >> save_to_silver
