"""
Module to transform tweeter's users related data and save
it into a csv ready to be loaded into a relational DB.
"""

from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_file
from etl_scripts.twitter.constants import USER_COLS_DICT
from etl_scripts.twitter.constants import USER_CSV_DIR
from etl_scripts.twitter.constants import USER_DATA_DIR
from etl_scripts.twitter.twitter_utils import build_dataframe
from etl_scripts.twitter.twitter_utils import timestamp_to_datetime


def transform_users_data():
    filepaths = get_data_filepaths(USER_DATA_DIR, "users", ".txt")
    for filepath in filepaths:
        df = build_dataframe(filepath)
        df.rename(columns=USER_COLS_DICT, inplace=True)
        df["collection_time"] = df.collection_time.apply(timestamp_to_datetime)
        df_to_csv(df, USER_CSV_DIR, "users")
        prefix_file(filepath, "transformed")


if __name__ == "__main__":
    pass
