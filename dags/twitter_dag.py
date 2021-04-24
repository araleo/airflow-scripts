from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from etl_scripts.twitter.botometer.transform_scores import transform_scores_data
from etl_scripts.twitter.botometer.load_scores import load_scores_data
from etl_scripts.twitter.botometer.score_users import score_users
from etl_scripts.twitter.load.hashtag_load import load_hashtags_data
from etl_scripts.twitter.load.media_load import load_medias_data
from etl_scripts.twitter.load.mention_load import load_mentions_data
from etl_scripts.twitter.load.tweet_load import load_tweets_data
from etl_scripts.twitter.load.url_load import load_urls_data
from etl_scripts.twitter.load.user_load import load_users_data
from etl_scripts.twitter.parse_tweets import parse_tweets_data
from etl_scripts.twitter.transform.entity_transform import transform_entities_data
from etl_scripts.twitter.transform.tweet_transform import transform_tweets_data
from etl_scripts.twitter.transform.user_transform import transform_users_data


with DAG(dag_id="twitter_dag", schedule_interval="@hourly", start_date=days_ago(1), catchup=False) as dag:

    parse_tweets_data = PythonOperator(
        task_id="parse_tweets_data",
        python_callable=parse_tweets_data
    )

    score_users = PythonOperator(
        task_id="score_users",
        python_callable=score_users
    )

    transform_users_data = PythonOperator(
        task_id="transform_users_data",
        python_callable=transform_users_data
    )

    transform_tweets_data = PythonOperator(
        task_id="transform_tweets_data",
        python_callable=transform_tweets_data
    )

    transform_entities_data = PythonOperator(
        task_id="transform_entities_data",
        python_callable=transform_entities_data
    )

    transform_scores_data = PythonOperator(
        task_id="transform_scores_data",
        python_callable=transform_scores_data
    )

    load_users_data = PythonOperator(
        task_id="load_users_data",
        python_callable=load_users_data
    )

    load_tweets_data = PythonOperator(
        task_id="load_tweets_data",
        python_callable=load_tweets_data
    )

    load_mentions_data = PythonOperator(
        task_id="load_mentions_data",
        python_callable=load_mentions_data
    )

    load_hashtags_data = PythonOperator(
        task_id="load_hashtags_data",
        python_callable=load_hashtags_data
    )

    load_urls_data = PythonOperator(
        task_id="load_urls_data",
        python_callable=load_urls_data
    )

    load_medias_data = PythonOperator(
        task_id="load_medias_data",
        python_callable=load_medias_data
    )

    load_scores_data = PythonOperator(
        task_id="load_scores_data",
        python_callable=load_scores_data
    )

    chain(
        parse_tweets_data,
        score_users,
        [
            transform_users_data,
            transform_tweets_data,
            transform_entities_data,
            transform_scores_data
        ],
        [
            load_users_data,
            load_tweets_data,
            [load_mentions_data, load_hashtags_data, load_medias_data, load_urls_data],
            load_scores_data
        ]
    )
