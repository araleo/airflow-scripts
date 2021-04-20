"""
Module to load an already prepared csv with subreddits data
into a relational postgresql database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.reddit.constants import ERROR_LOG_PATH
from etl_scripts.reddit.constants import SUBS_TRANSFORMED_DIR


ERRORS = []


def load_subs_data():
    df = load_dataframes(SUBS_TRANSFORMED_DIR, "reddit", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "reddit", "sub_counts", ERRORS)
    except SQLAlchError:
        pass
    else:
        prefix_files(SUBS_TRANSFORMED_DIR, "loaded")

    log_errors(ERROR_LOG_PATH, "reddit.subs_load", ERRORS)


if __name__ == '__main__':
    pass
