"""
Module to load raw tweets downloaded from the API, parse them
according to the project's bussiness rules and save as JSONs
"""

from datetime import datetime
import json
import os

from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.twitter.constants import RAW_DIR
from etl_scripts.twitter.constants import ENTITIES_DATA_DIR
from etl_scripts.twitter.constants import TWEET_DATA_DIR
from etl_scripts.twitter.constants import USER_DATA_DIR
from etl_scripts.twitter.filter_json import filter_tweet
from etl_scripts.twitter.twitter_utils import load_tweets


PROCESSED_TWEETS = []
USERS = []
TWEETS = []
COUNTS = []
ENTITIES = []


def save_as_json(tweet):
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    with open(f"tweet_{now}.json", "w") as f:
        json.dump(tweet, f)


def save_file(filepath, data):
    if not data:
        return
    with open(filepath, "w") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def save_parsed_tweets():
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

    users_path = os.path.join(USER_DATA_DIR, f"users_{now}.txt")
    tweets_path = os.path.join(TWEET_DATA_DIR, f"tweets_{now}.txt")
    counts_path = os.path.join(TWEET_DATA_DIR, f"counts_{now}.txt")
    entities_path = os.path.join(ENTITIES_DATA_DIR, f"entities_{now}.txt")

    save_file(users_path, USERS)
    save_file(tweets_path, TWEETS)
    save_file(counts_path, COUNTS)
    save_file(entities_path, ENTITIES)


def separate_user(tweet):
    user = tweet.get("user_core")
    user["collection_time"] = tweet.get("collection_time_ts_ms")
    USERS.append(user)


def separate_entity(tweet, entity):
    for _entity in tweet.get(entity, []):
        _entity["collection_time"] = tweet.get("collection_time_ts_ms")
        _entity["type"] = entity
        ENTITIES.append(_entity)


def separate_entities(tweet):
    tweet_entities = ["user_mentions", "urls", "hashtags", "medias"]
    for entity in tweet_entities:
        separate_entity(tweet, entity)


def separate_counts(tweet):
    t = tweet.get("tweet_counts")
    t["collection_time"] = tweet.get("collection_time_ts_ms")
    COUNTS.append(t)


def separate_tweet(tweet):
    t = tweet.get("tweet_core")
    t["collection_time"] = tweet.get("collection_time_ts_ms")
    TWEETS.append(t)


def separate_users_tweets():
    for tweet in PROCESSED_TWEETS:
        separate_user(tweet)
        separate_entities(tweet)
        separate_tweet(tweet)
        separate_counts(tweet)


def parse_tweet(tweet, collection_time_ts_ms=None):
    if collection_time_ts_ms is None:
        collection_time_ts_ms = tweet.get("timestamp_ms")

    filtered = filter_tweet(tweet)
    filtered["collection_time_ts_ms"] = collection_time_ts_ms
    PROCESSED_TWEETS.append(filtered)

    if filtered["tweet_core"].get("quoted_id"):
        parse_tweet(tweet.get("quoted_status"), collection_time_ts_ms)

    if filtered["tweet_core"].get("retweeted_id"):
        parse_tweet(tweet.get("retweeted_status"), collection_time_ts_ms)


def parse_tweets_data():
    tweet_files = get_data_filepaths(RAW_DIR, "stf", ".txt")
    for _file in tweet_files:
        for tweet in load_tweets(_file):
            parse_tweet(tweet)
    separate_users_tweets()
    save_parsed_tweets()
    prefix_files(RAW_DIR, "parsed")


if __name__ == '__main__':
    pass
