from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# Later we need to substitute this absolute path for an env variable
utils_path = '/Users/douglasmelo/Documents/projects/indicium/code-challenge/indicium-challenge-pipeline/utils'
sys.path.insert(0, utils_path)

from createDirectories import organize_csv_files



dag = DAG(
    dag_id="meltano_csv_pipeline",
    start_date=datetime(2023, 10, 1),
    schedule_interval="@daily",
    catchup=False,
)

meltano_command_csv = """
cd /Users/douglasmelo/Documents/projects/indicium/code-challenge/indicium-challenge-pipeline &&
meltano run tap-csv target-csv
"""


meltano_command_postgres = """
cd /Users/douglasmelo/Documents/projects/indicium/code-challenge/indicium-challenge-pipeline &&
meltano run tap-postgres target-csv
"""

run_meltano_extract_csv = BashOperator(
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


run_meltano_extract_postgres = BashOperator(
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


run_meltano_extract_csv >> organize_csv_task >> run_meltano_extract_postgres >> organize_postgres_task