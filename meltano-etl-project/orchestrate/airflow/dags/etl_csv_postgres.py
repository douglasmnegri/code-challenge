from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import os

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'northwind_elt_structured',
    default_args=default_args,
    description='Extracts data from multiple sources, organize CSVs into date-partitioned directories and load them in a new database',
    schedule_interval='@daily',
    catchup=False,
)

# Meltano Extraction: Extracts and loads order_details.csv inside the csv directory
extract_csv = BashOperator(
    task_id='extract_csv',
    bash_command=f'cd {PROJECT_ROOT} && meltano run tap-csv--dir target-csv--dir',
    dag=dag,
)

# Meltano Extraction: Extracts and loads all tables from northwind database inside the postgres directory
extract_postgres = BashOperator(
    task_id='extract_postgres',
    bash_command=f'cd {PROJECT_ROOT} && meltano run tap-postgres target-csv--pg',
    dag=dag,
)

# Organize Files
organize_files_task = BashOperator(
    task_id='organize_files',
    bash_command=(
        f'python {PROJECT_ROOT}/scripts/file_organizer.py '
        f'"{PROJECT_ROOT}" '
        '"{{ ds }}"'
    ),
    dag=dag,
)

# Upload files into processed_data database
run_pipeline_task = BashOperator(
    task_id='run_csv_pipeline',
    bash_command=(
        f'python {PROJECT_ROOT}/scripts/upload_files.py '
        f'"{PROJECT_ROOT}" '
        '"{{ ds }}"'
    ),
    dag=dag,
)

extract_csv >> extract_postgres >> organize_files_task >> run_pipeline_task
