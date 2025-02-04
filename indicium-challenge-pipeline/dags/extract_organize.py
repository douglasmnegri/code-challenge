from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG
import os
import sys
from dotenv import load_dotenv

load_dotenv()
utils_path = os.getenv("UTILS_PATH")
project_path = os.getenv("PROJECT_PATH")

print("Project's Path: ", project_path) # Check if correct project path was passed to the .env file (Absolute path is recommended)
print("Utils's Path: ", project_path) # Check if correct utils path was passed to the .env file

sys.path.insert(0, utils_path)
from directories import organize_csv_files

dag = DAG(
    dag_id="meltano_csv_pipeline",
    start_date=datetime(2023, 10, 1),
    schedule_interval="@daily",
    catchup=False,
)

meltano_command_csv = f"""
cd {project_path} &&
meltano config tap-csv set files '[{{"entity": "order_details", "path": "../data/order_details.csv", "keys": ["order_id"], "delimiter": ","}}]' &&
meltano run tap-csv target-csv
"""


meltano_command_postgres = f"""
cd {project_path} &&
meltano run tap-postgres target-csv
"""

extract_csv = BashOperator(
    task_id="extract_to_csv",
    bash_command=meltano_command_csv,
    dag=dag,
)

organize_csv_task = PythonOperator(
    task_id="organize_csv_files",
    python_callable=organize_csv_files,
    op_args=["output/csv"],
    dag=dag,
)


extract_postgres = BashOperator(
    task_id="extract_to_postgres",
    bash_command=meltano_command_postgres,
    dag=dag,
)

organize_postgres_task = PythonOperator(
    task_id="organize_postgres_files",
    python_callable=organize_csv_files,
    op_args=["output/postgres"],
    dag=dag,
)


extract_csv >> organize_csv_task >> extract_postgres >> organize_postgres_task
