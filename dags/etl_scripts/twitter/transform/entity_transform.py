"""
Module to transform tweets' entities data and save it
into a csv ready to be loaded into a relational DB
"""

import pandas as pd

from etl_scripts.twitter.constants import ENTITIES_CSV_DIR
from etl_scripts.twitter.constants import ENTITIES_DATA_DIR
from etl_scripts.twitter.constants import HASHTAG_COLS_DICT
from etl_scripts.twitter.constants import MEDIA_COLS_DICT
from etl_scripts.twitter.constants import MENTION_COLS_DICT
from etl_scripts.twitter.constants import URL_COLS_DICT
from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_file
from etl_scripts.twitter.twitter_utils import load_tweets
from etl_scripts.twitter.twitter_utils import timestamp_to_datetime


ENTITIES = {
    "user_mentions": [],
    "urls": [],
    "medias": [],
    "hashtags": []
}

COLUMNS = {
    "user_mentions": MENTION_COLS_DICT,
    "hashtags": HASHTAG_COLS_DICT,
    "medias": MEDIA_COLS_DICT,
    "urls": URL_COLS_DICT
}


def transform_entity(entity, name):
    df = pd.DataFrame(entity)
    df.drop(columns=["type"], inplace=True)
    df["collection_time"] = df.collection_time.apply(timestamp_to_datetime)
    df.rename(columns=COLUMNS.get(name), inplace=True)
    df_to_csv(df, ENTITIES_CSV_DIR, name)


def transform_entities():
    for name, entity in ENTITIES.items():
        if entity:
            transform_entity(entity, name)


def separate_entities(entities):
    for entity in entities:
        entity_type = entity.get("type")
        ENTITIES[entity_type].append(entity)


def transform_entities_data():
    filepaths = get_data_filepaths(ENTITIES_DATA_DIR, "entities", ".txt")
    for filepath in filepaths:
        entities = load_tweets(filepath)
        separate_entities(entities)
        transform_entities()
        prefix_file(filepath, "transformed")


if __name__ == "__main__":
    pass
