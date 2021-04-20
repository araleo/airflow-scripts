"""
Module to transform subreddits data
"""

from datetime import datetime

from etl_scripts.DB.PostgresConn import PostgresConn
from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.reddit.constants import SUBS_FILTER_COLUMNS
from etl_scripts.reddit.constants import SUBS_HEADERS
from etl_scripts.reddit.constants import SUBS_RAW_DIR
from etl_scripts.reddit.constants import SUBS_TRANSFORMED_DIR


def map_subs_ids(subs_names, subs_titles):
    db = PostgresConn()
    subs_ids = {
        name: db.get_id_or_create("nome", [name], ["id"], "reddit", "subreddits", ["nome", "titulo"], [name, title])
        for name, title in zip(subs_names, subs_titles)
    }
    db.close()
    return subs_ids


def transform_data(df):
    df["ID_SUB"] = df.DISPLAY_NAME.map(map_subs_ids(list(df.DISPLAY_NAME.unique()), list(df.TITLE.unique())))
    df["COLLECTION_TIME"] = df.TIMESTAMP.apply(datetime.fromtimestamp)
    df_export = df.loc[:, SUBS_FILTER_COLUMNS]
    df_export.rename(str.lower, axis="columns", inplace=True)
    return df_export


def transform_subs_data():
    df = load_dataframes(SUBS_RAW_DIR, "reddit", ".txt", SUBS_HEADERS)
    if df is None:
        return

    df = transform_data(df)
    df_to_csv(df, SUBS_TRANSFORMED_DIR, "reddit_subs")
    prefix_files(SUBS_RAW_DIR, "transformed")


if __name__ == "__main__":
    pass
