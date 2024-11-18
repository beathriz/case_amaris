# case_amaris
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
    
 6. Monitoring/Alerting: Dag de alerta para e-mail
  Configuração do SMTP: O Airflow utiliza o protocolo SMTP para enviar e-mails.
  Defini o servidor SMTP e as credenciais no arquivo airflow.cfg (conforme imagem)

  Opções para rquitetura mais complexa: 
  - Callbacks Customizados
  - Serviços de monitoramento: Datadog, Prometheus, ou Grafana

  7. Repository: https://github.com/beathriz/case_amaris

  8. Cloud Services: MinIO - conectado no Docker


