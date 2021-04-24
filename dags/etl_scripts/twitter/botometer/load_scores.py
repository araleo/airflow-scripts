"""
Moduloe to load scored users tweets into a postgreSQL database
"""

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import add_prefix_to_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.twitter.constants import ERROR_LOG_PATH
from etl_scripts.twitter.constants import SCORES_CSV_DIR


ERRORS = []


def load_scores_data():
    df = load_dataframes(SCORES_CSV_DIR, "scores", ".csv")
    if df is None:
        return

    try:
        sqlalch_load(df, "twitter", "scored_tweets", ERRORS)
    except SQLAlchError:
        pass
    else:
        add_prefix_to_files(SCORES_CSV_DIR, "scores", "loaded")

    log_errors(ERROR_LOG_PATH, "twitter.scored_tweets", ERRORS)


if __name__ == "__main__":
    pass
