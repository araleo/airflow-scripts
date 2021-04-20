"""
Module to load an already prepared csv with g1 news data
into a relational postgresql database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.g1.constants import TRANSFORMED_DIR
from etl_scripts.g1.constants import ERROR_LOG_PATH


ERRORS = []


def load_g1_data():
    df = load_dataframes(TRANSFORMED_DIR, "g1", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "noticias", "noticias", ERRORS)
    except SQLAlchError:
        pass
    else:
        prefix_files(TRANSFORMED_DIR, "loaded")

    log_errors(ERROR_LOG_PATH, "g1.load", ERRORS)


if __name__ == "__main__":
    pass
