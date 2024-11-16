# case_amaris
Creation of Data Lake Architecture

Preparation: 
  1. Docker: Download > docker --version > docker-compose --version

- Airflow: 
  1. Configurar o ambiente usando o docker-compose.yml
  2. Baixar o arquivo base do Airflow: curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
  3. Criar os diretórios:
    mkdir dags logs plugins
    echo -e "AIRFLOW_UID=$(id -u)" > .env
  4. Subir o Airflow: docker-compose up -d

- PySpark 
  1. Optei por criar um ambiente virtual para separar as config.
    .\venv\Scripts\activate  
  2. Instalar no ambiente: pip install pyspark

- Python
  1. python --version

- VS Code with extensions: Docker /  Python /  Remote Containers /  GitHub

Settings
  1. API: <https://api.openbrewerydb.org/breweries> 

  2. Orchestration Tool: Apache Airflow

  3. Language: Python and PySpark

  4. Containerization: Docker 

  5. Data Lake Architecture: Delta Lake

    a. Bronze Layer: 
    b. Silver Layer:
    c. Gold Layer: 



