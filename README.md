
# Indicium Tech Code Challenge 

Code challenge for Software Developer with focus in data projects.

## Technologies Used
- Python (Version **3.9.6**)
- Apache Airflow (Version **2.10.4**)
- Meltano (Version **3.6.0**)
- Docker (Version **27.3.1**)
- Docker Compose (Version **2.29.7**)


## Installation

1. Python Environment (Recommended)

```bash
python3 -m venv venv_name
source venv_name/bin/activate  # macOS/Linux
venv_name\Scripts\activate     # Windows (PowerShell)
```

2. Meltano

```bash
  pip install meltano
  meltano install
```

3. Airflow


```bash
  export AIRFLOW_HOME=~/airflow  # Can be run inside the project
  pip install apache-airflow
```

- After installing Airflow, open the airflow.cfg file and update the dags_folder path to point to your project's DAGs directory:

```bash
dags_folder = /path/to/your_project/dags
```

- Initiate the database 
```bash
airflow db init
```

- Run your credentials

```bash
airflow users create \
--username <your_username> \
--firstname <first_name> \
--lastname <last_name> \
--role Admin \
--email <seu-email>
```


4. psycopg2 (Needed for query)
```bash
pip install psycopg2-binary
```


## Running the project

1. If you've installed the python virtual environment, activate it.

2. Start the docker-compose.yml file that contains both databases:

```bash
docker-compose up --build
docker-compose up -d
```

3. Start the airflow on two different terminals and make sure the dags folder path is in line with `airflow.cfg`:

```bash
airflow webserver --port 8080
airflow scheduler
```

4. Access Airflow UI
- Open your browser and go to: 🔗 http://localhost:8080

5. Run dags
In the Airflow UI, trigger both DAGs:
- `meltano_csv_pipeline`
- `meltano_pipeline_dag`

## Aiflow running a DAG

![Airflow running the extraction DAG](./gif/airflow.gif.gif)
