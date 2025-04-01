from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import json
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dbt_gcp_execution_corrected",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    catchup=False,
) as dag:
    gcs_bucket = "dbt_airflow_test"
    dbt_project_folder = "mytest"
    dbt_profile_name = "mytest"

    dbt_clone = BashOperator(
        task_id="clone_dbt_project",
        bash_command=f"gsutil -m cp -r gs://{gcs_bucket}/{dbt_project_folder} /home/airflow",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd /home/airflow/{dbt_project_folder} && dbt run --profiles-dir . --profile {dbt_profile_name}",
    )

    dbt_clone >> dbt_run
