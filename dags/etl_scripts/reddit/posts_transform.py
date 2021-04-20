"""
Module to transform reddit posts data
"""

from datetime import datetime

from etl_scripts.DB.PostgresConn import PostgresConn
from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.reddit.constants import POSTS_DB_COLUMNS
from etl_scripts.reddit.constants import POSTS_FILTER_COLUMNS
from etl_scripts.reddit.constants import POSTS_HEADERS
from etl_scripts.reddit.constants import POSTS_RAW_DIR
from etl_scripts.reddit.constants import POSTS_TRANSFORMED_DIR
from etl_scripts.reddit.subs_transform import map_subs_ids


def map_users_ids(users):
    db = PostgresConn()
    users_ids = db.filter("name", users, ["id", "name"], "reddit", "users")
    db.close()
    return {name: _id for _id, name in users_ids}


def transform_data(df):
    df["ID_SUB"] = df.SUBREDDIT.map(map_subs_ids(list(df.SUBREDDIT.unique()), list(df.SUBREDDIT.unique())))
    df["ID_USER"] = df.AUTHOR.map(map_users_ids(set(user.strip() for user in df.AUTHOR.unique()))).convert_dtypes()
    df["CREATED_TS"] = df.CREATED.apply(datetime.fromtimestamp)
    df["COLLECTION_TIME"] = df.TIMESTAMP.apply(datetime.fromtimestamp)
    df["GILDED_BOOL"] = df.GILDED.apply(bool)
    return df


def filter_data(df):
    df_export = df.loc[:, POSTS_FILTER_COLUMNS]
    df_export.columns = POSTS_DB_COLUMNS
    df_export.dropna(subset=["id_user"], inplace=True)
    return df_export


def transform_posts_data():
    df = load_dataframes(POSTS_RAW_DIR, "reddit", ".txt", POSTS_HEADERS)
    if df is None:
        return

    df = transform_data(df)
    df = filter_data(df)

    df_to_csv(df, POSTS_TRANSFORMED_DIR, "reddit_posts")
    prefix_files(POSTS_RAW_DIR, "transformed")


if __name__ == "__main__":
    pass
