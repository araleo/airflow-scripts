from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from etl_scripts.reddit.posts_load import load_posts_data
from etl_scripts.reddit.subs_load import load_subs_data
from etl_scripts.reddit.users_load import load_users_data
from etl_scripts.reddit.posts_transform import transform_posts_data
from etl_scripts.reddit.subs_transform import transform_subs_data
from etl_scripts.reddit.users_transform import transform_users_data
from etl_scripts.reddit.extract.main import extract_reddit_data


with DAG(dag_id="reddit_dag", schedule_interval="@hourly", start_date=days_ago(1), catchup=False) as dag:

    extract_reddit_data = PythonOperator(
        task_id="extract_reddit_data",
        python_callable=extract_reddit_data
    )

    transform_subs_data = PythonOperator(
        task_id="transform_subs_data",
        python_callable=transform_subs_data
    )

    load_subs_data = PythonOperator(
        task_id="load_subs_data",
        python_callable=load_subs_data
    )

    transform_users_data = PythonOperator(
        task_id="transform_users_data",
        python_callable=transform_users_data
    )

    load_users_data = PythonOperator(
        task_id="load_users_data",
        python_callable=load_users_data
    )

    transform_posts_data = PythonOperator(
        task_id="transform_posts_data",
        python_callable=transform_posts_data
    )

    load_posts_data = PythonOperator(
        task_id="load_posts_data",
        python_callable=load_posts_data
    )

    chain(
        extract_reddit_data,
        [transform_subs_data, transform_users_data],
        [load_subs_data, load_users_data],
        transform_posts_data,
        load_posts_data
    ) 