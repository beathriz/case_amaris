# case_breweries
Creation of Data Lake Architecture

Preparation: 
  1. Docker: Download > docker --version > docker-compose --version

- Airflow: 
   Configurar o ambiente usando o docker-compose.yml
   Baixar o arquivo base do Airflow: curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
   Criar os diretórios:
      mkdir dags logs plugins
      echo -e "AIRFLOW_UID=$(id -u)" > .env
   Subir o Airflow: docker-compose up -d

- Python
   python --version

- VS Code with extensions: Docker /  Python /  Remote Containers /  GitHub

Settings
  1. API: <https://api.openbrewerydb.org/breweries> 

  2. Orchestration Tool: Apache Airflow

  3. Language: Python and PySpark

  4. Containerization: Docker 

  5. Data Lake Architecture: Volum in Docker

    a. Bronze Layer: Used for storing data in its original format
    b. Silver Layer: Data is transformed into a columnar format like Parquet or Delta and partitioned by brewery location.
    c. Gold Layer: Processed data in an aggregated view with the number of breweries by type and location, in .parquet format
    
  6. Monitoring/Alert: Email alert day
  SMTP Configuration: Airflow uses the SMTP protocol to send emails.
  Define the SMTP server and credentials in the airflow.cfg file (as shown in the image)

  Options for more complex architecture: 
  - Customized callbacks
  - Monitoring services: Datadog, Prometheus, or Grafana

  7. Repository: github.com/beathriz/case_breweries

  8. Cloud Services: Google Drive with rclone.
       Rclone - is a command-line software designed to manage, synchronize, and transfer files between local systems and cloud storage services.


