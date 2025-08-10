from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from Extraction import run_extraction
from Transformation import run_transformation
from Loading import run_loading

default_args ={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 10),
    'email': 'dibanga2800@gmail.com',
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'zipco_foods_pipeline',
    default_args=default_args,
    description='ETL pipeline for Zipco Foods',
)

extraction = PythonOperator(
    task_id='extraction',
    python_callable=run_extraction,
    dag=dag
)

transformation = PythonOperator(
    task_id='transformation',
    python_callable=run_transformation,
    dag=dag
)

loading = PythonOperator(
    task_id='loading',
    python_callable=run_loading,
    dag=dag
)

extraction >> transformation >> loading