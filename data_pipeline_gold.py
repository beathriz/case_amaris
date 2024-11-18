from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline_gold',
    default_args=default_args,
    description='Pipeline to create Gold layer from Silver layer',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

def create_gold_layer():
    try:
        print("Iniciando criação da camada Gold...")

        silver_path = "/data/silver"
        gold_path = "/data/gold"

        # Certifica-se de que o diretório Gold existe
        os.makedirs(gold_path, exist_ok=True)
        print(f"Diretório Gold garantido em: {gold_path}")

        spark = SparkSession.builder \
            .appName("Gold Layer Aggregation") \
            .getOrCreate()
        print("Sessão Spark inicializada.")

        # Lê os dados da camada Silver
        df_silver = spark.read.parquet(silver_path)
        print(f"Dados carregados da camada Silver: {silver_path}")
        df_gold = df_silver.groupBy("state", "brewery_type").agg(
            count("*").alias("brewery_count")
        )
        print("Agregação realizada com sucesso.")

        # Escreve os dados na camada Gold
        df_gold.write.parquet(gold_path, mode="overwrite")
        print(f"Camada Gold criada com sucesso em: {gold_path}")

    except Exception as e:
        print(f"Erro ao criar a camada Gold: {e}")
        raise

create_gold_task = PythonOperator(
    task_id='create_gold_layer',
    python_callable=create_gold_layer,
    dag=dag,
)
