"""
Module to load tweets hashtags data into a postgreSQL database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import add_prefix_to_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.twitter.constants import ERROR_LOG_PATH
from etl_scripts.twitter.constants import ENTITIES_CSV_DIR


ERRORS = []


def load_hashtags_data():
    df = load_dataframes(ENTITIES_CSV_DIR, "hashtags", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "twitter", "hashtags", ERRORS)
    except SQLAlchError:
        pass
    else:
        add_prefix_to_files(ENTITIES_CSV_DIR, "hashtags", "loaded")

    log_errors(ERROR_LOG_PATH, "twitter.hashtags_load", ERRORS)


if __name__ == "__main__":
    pass
