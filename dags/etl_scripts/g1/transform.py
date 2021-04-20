"""
Module to transform data scrapped from g1's website.
"""

from datetime import datetime

from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import load_dataframes
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.g1.constants import DB_COLUMNS
from etl_scripts.g1.constants import FILTER_COLUMNS
from etl_scripts.g1.constants import HEADERS
from etl_scripts.g1.constants import RAW_DIR
from etl_scripts.g1.constants import TRANSFORMED_DIR
from etl_scripts.g1.db import insert_new_categories
from etl_scripts.g1.db import query_categories_ids
from etl_scripts.g1.db import query_page_id_or_create
from etl_scripts.g1.db import select_all_urls


def update_categories_table(categories):
    data = query_categories_ids(categories)
    registered = set(cat for _, cat in data)
    to_insert = categories.difference(registered)
    if to_insert:
        insert_new_categories(to_insert)


def map_categories_ids(categories):
    categories = set(cat.strip() for cat in categories)
    update_categories_table(categories)
    data = query_categories_ids(categories)
    return {cat: _id for _id, cat in data}


def generate_timestamp(date_hour):
    return datetime.strptime(date_hour, "%d/%m/%Y %Hh%M")


def get_fields_names():
    return dict(zip(FILTER_COLUMNS, DB_COLUMNS))


def append_columns(df):
    df["ID_CATEGORIA"] = df.PAGE.map(map_categories_ids(df.PAGE))
    df["ID_PAGINA"] = query_page_id_or_create("G1")
    df["DATAHORA"] = df.DATE.apply(generate_timestamp)
    return df


def transform_data(df):
    df = append_columns(df)
    df_export = df.loc[:, FILTER_COLUMNS]
    df_export.rename(get_fields_names(), axis="columns", inplace=True)
    return df_export


def filter_dataframe(df):
    df = df.loc[df.PAGE != "Null"]
    df.drop_duplicates(subset=["URL"], keep="last", inplace=True)
    already_loaded = select_all_urls()
    return df[~df["URL"].isin(already_loaded)]


def transform_g1_data():
    df = load_dataframes(RAW_DIR, "g1", "txt", HEADERS)
    if df is None:
        return

    df = filter_dataframe(df)

    if not df.empty:
        df = transform_data(df)
        df_to_csv(df, TRANSFORMED_DIR, "g1")

    prefix_files(RAW_DIR, "transformed")


if __name__ == "__main__":
    pass
