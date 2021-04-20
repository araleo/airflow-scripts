from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from etl_scripts.g1.scrap import g1_scrapper
from etl_scripts.g1.transform import transform_g1_data
from etl_scripts.g1.load import load_g1_data


with DAG(dag_id="g1_dag", schedule_interval=timedelta(hours=8), start_date=days_ago(1), catchup=False) as dag:

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=g1_scrapper
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_g1_data
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=load_g1_data
    )

    extract_data >> transform_data >> load_data
