"""
Module to transform reddit users data
"""

from datetime import datetime

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.DB.PostgresConn import PostgresConn
from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import log_errors
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.global_utils.global_utils import sqlalch_load
from etl_scripts.reddit.constants import ERROR_LOG_PATH
from etl_scripts.reddit.constants import USERS_DB_COLUMNS
from etl_scripts.reddit.constants import USERS_FILTER_COLUMNS
from etl_scripts.reddit.constants import USERS_HEADERS
from etl_scripts.reddit.constants import USERS_RAW_DIR
from etl_scripts.reddit.constants import USERS_TRANSFORMED_DIR
from etl_scripts.reddit.constants import USER_STATS_DB_COLUMNS
from etl_scripts.reddit.constants import USER_STATS_FILTER_COLUMNS


ERRORS = []


def query_all_users(users):
    db = PostgresConn()
    _ids = db.filter("reddit_id", users, ["id", "reddit_id"], "reddit", "users")
    db.close()
    return _ids


def find_unregistered_users(df):
    users = set(user.strip() for user in df.ID.unique())
    registered = set(user for _, user in query_all_users(users))
    return users.difference(registered)


def load_new_users(df):
    try:
        sqlalch_load(df, "reddit", "users", ERRORS)
    except SQLAlchError:
        pass


def register_new_users(df):
    df.drop_duplicates(subset=["ID"], keep="last", inplace=True)
    df_export = df.loc[:, USERS_FILTER_COLUMNS]
    df_export.columns = USERS_DB_COLUMNS
    load_new_users(df_export)


def update_users_table(df):
    unregistered = find_unregistered_users(df)
    new_users_df = df.loc[df.ID.isin(unregistered)]
    register_new_users(new_users_df)


def map_users_ids(df):
    update_users_table(df)
    users_data = query_all_users(set(user.strip() for user in df.ID.unique()))
    return {reddit_id: _id for _id, reddit_id in users_data}


def transform_data(df):
    df["CREATED_TS"] = df.CREATED_UTC.apply(datetime.utcfromtimestamp)
    df["COLLECTION_TIME"] = df.TIMESTAMP.apply(datetime.fromtimestamp)
    df["ID_BANCO"] = df.ID.map(map_users_ids(df))
    return df


def filter_users_stats(df):
    df_export = df.loc[:, USER_STATS_FILTER_COLUMNS]
    df_export.columns = USER_STATS_DB_COLUMNS
    return df_export


def transform_users_data():
    df = load_dataframes(USERS_RAW_DIR, "reddit", ".txt", USERS_HEADERS)
    if df is None:
        return

    df = transform_data(df)
    df = filter_users_stats(df)

    df_to_csv(df, USERS_TRANSFORMED_DIR, "reddit_user_stats")
    prefix_files(USERS_RAW_DIR, "transformed")
    log_errors(ERROR_LOG_PATH, "reddit.users_transform", ERRORS)


if __name__ == "__main__":
    pass
