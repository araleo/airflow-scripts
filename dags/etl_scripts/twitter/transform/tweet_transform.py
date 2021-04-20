"""
Module to transform tweets' data and
prepare it to be loaded into a relational DB.
"""

from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_file
from etl_scripts.twitter.constants import TWEET_CSV_DIR
from etl_scripts.twitter.constants import TWEET_DATA_DIR
from etl_scripts.twitter.twitter_utils import build_dataframe
from etl_scripts.twitter.twitter_utils import timestamp_to_datetime


def transform_tweets_data():
    filepaths = get_data_filepaths(TWEET_DATA_DIR, "tweets", ".txt")
    for filepath in filepaths:
        df = build_dataframe(filepath)
        df.rename(columns={"id": "twitter_id"}, inplace=True)
        df["collection_time"] = df.collection_time.apply(timestamp_to_datetime)
        df["timestamp_ms"] = df.timestamp_ms.apply(timestamp_to_datetime)
        df_to_csv(df, TWEET_CSV_DIR, "tweets")
        prefix_file(filepath, "transformed")

        
if __name__ == "__main__":
    pass
