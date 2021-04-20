"""
Module to load tweets urls data into a postgreSQL database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import add_prefix_to_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.twitter.constants import ERROR_LOG_PATH
from etl_scripts.twitter.constants import ENTITIES_CSV_DIR


ERRORS = []


def load_urls_data():
    df = load_dataframes(ENTITIES_CSV_DIR, "urls", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "twitter", "urls", ERRORS)
    except SQLAlchError:
        pass
    else:
        add_prefix_to_files(ENTITIES_CSV_DIR, "urls", "loaded")

    log_errors(ERROR_LOG_PATH, "twitter.urls_load", ERRORS)


if __name__ == "__main__":
    pass
