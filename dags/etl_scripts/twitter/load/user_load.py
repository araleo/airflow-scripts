"""
Module to load user data into a postgreSQL database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.twitter.constants import ERROR_LOG_PATH
from etl_scripts.twitter.constants import USER_CSV_DIR


ERRORS = []


def load_users_data():
    df = load_dataframes(USER_CSV_DIR, "users", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "twitter", "users", ERRORS)
    except SQLAlchError:
        pass
    else:
        prefix_files(USER_CSV_DIR, "loaded")

    log_errors(ERROR_LOG_PATH, "twitter.users_load", ERRORS)


if __name__ == "__main__":
    pass
