# Airflow

- Airflow is a batch workflow orchestration platform. The airflow framework contains operators to connect with many technologies and is easily extensible to connect with a new technology. If your workflows have a clear start and end, and run at regular intervals, they can be programmed as an Airflow DAG.
- If you prefer coding over clicking, Airflow is the tool for you. Workflows are defined as Python code.
- But Airflow was built for finite batch workflows. While the CLI and REST API do allow triggering workflows, Airflow was not built for infinitely running event-based workflows. --> Airflow is not a streaming solution.

## Cloud Composer in GCP

### Data stored in Cloud Storage

| Folder  | Storage path             | Mapped directory          |
| ------- | ------------------------ | ------------------------- |
| DAG     | gs://bucket-name/dags    | /home/airflow/gcs/dags    |
| Plugins | gs://bucket-name/plugins | /home/airflow/gcs/plugins |
