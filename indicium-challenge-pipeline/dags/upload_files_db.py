from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
project_path = os.getenv("PROJECT_PATH")
print("Project's Path: ", project_path)


def run_meltano_command(**kwargs):
    if 'date' in kwargs['dag_run'].conf:
        past_date = kwargs['dag_run'].conf['date']
    else:
        past_date = kwargs['execution_date'].strftime('%Y-%m-%d')

    meltano_command_csv = f"""
    cd {project_path} &&
    meltano config tap-csv set files '[{{"entity": "order_details", "path": "output/csv/order_details/{past_date}/order_details.csv", "keys": ["order_id"], "delimiter": ","}}]' &&
    meltano run tap-csv target-postgres
    """

    meltano_command_postgres = f"""
        cd {project_path} &&
        meltano config tap-csv set files '[{{"entity": "orders", "path": "output/postgres/orders/{past_date}/public-orders.csv", "keys": ["order_id"], "delimiter": ","}}]' &&
        meltano run tap-csv target-postgres-orders
    """

    subprocess.run(meltano_command_csv, shell=True, check=True)
    subprocess.run(meltano_command_postgres, shell=True, check=True)


with DAG(
    'meltano_pipeline_dag',
    default_args={'owner': 'airflow'},
    description='Extracts data from the correct folder and uploads to the processed_data db',
    schedule_interval=None,
    start_date=datetime(2025, 2, 3),
    catchup=False,
) as dag:

    run_meltano = PythonOperator(
        task_id='run_meltano_command',
        python_callable=run_meltano_command,

        provide_context=True,
    )

    run_meltano
