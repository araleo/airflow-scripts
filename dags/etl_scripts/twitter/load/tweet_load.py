"""
Module to load tweets data into a postgreSQL database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import add_prefix_to_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.twitter.constants import ERROR_LOG_PATH
from etl_scripts.twitter.constants import TWEET_CSV_DIR


ERRORS = []


def load_tweets_data():
    df = load_dataframes(TWEET_CSV_DIR, "tweets", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "twitter", "tweets", ERRORS)
    except SQLAlchError:
        pass
    else:
        add_prefix_to_files(TWEET_CSV_DIR, "tweets", "loaded")

    log_errors(ERROR_LOG_PATH, "twitter.tweets_load", ERRORS)


if __name__ == "__main__":
    pass
