"""
Module to load raw tweets downloaded from the API, parse them
according to the project's bussiness rules and save as JSONs
"""

from datetime import datetime
import os

from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_files
from etl_scripts.twitter.constants import ENTITIES_DATA_DIR
from etl_scripts.twitter.botometer.constants import MAX_TWEETS_PER_SCREEN_NAME
from etl_scripts.twitter.botometer.constants import MIN_TWEET_LENGTH
from etl_scripts.twitter.constants import RAW_DIR
from etl_scripts.twitter.constants import SCORING_DATA_DIR
from etl_scripts.twitter.constants import SCREEN_NAMES
from etl_scripts.twitter.constants import TWEET_DATA_DIR
from etl_scripts.twitter.constants import USER_DATA_DIR
from etl_scripts.twitter.filter_json import filter_tweet
from etl_scripts.twitter.twitter_utils import load_tweets
from etl_scripts.twitter.twitter_utils import save_file


PROCESSED_TWEETS = []
USERS = []
TWEETS = []
ENTITIES = []
SCORING_TWEETS = {screen_name: [] for screen_name in SCREEN_NAMES}


def save_parsed_tweets():
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

    users_path = os.path.join(USER_DATA_DIR, f"users_{now}.txt")
    tweets_path = os.path.join(TWEET_DATA_DIR, f"tweets_{now}.txt")
    entities_path = os.path.join(ENTITIES_DATA_DIR, f"entities_{now}.txt")

    save_file(users_path, USERS)
    save_file(tweets_path, TWEETS)
    save_file(entities_path, ENTITIES)


def save_chosen_for_scoring():
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    for screen_name, tweets in SCORING_TWEETS.items():
        screen_names_path = os.path.join(SCORING_DATA_DIR, f"score_{screen_name}_{now}.txt")
        save_file(screen_names_path, tweets)


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


def separate_tweet(tweet):
    t = tweet.get("tweet_core")
    t["collection_time"] = tweet.get("collection_time_ts_ms")
    TWEETS.append(t)


def separate_users_tweets():
    for tweet in PROCESSED_TWEETS:
        separate_user(tweet)
        separate_entities(tweet)
        separate_tweet(tweet)


def parse_tweet(tweet):
    filtered = filter_tweet(tweet)
    filtered["collection_time_ts_ms"] = tweet.get("timestamp_ms")
    choose_user_mentions(filtered)
    PROCESSED_TWEETS.append(filtered)


def check_if_tweet_is_valid_for_scoring(tweet):
    core = tweet["tweet_core"]
    text = core.get("text", "")
    return len(text) > MIN_TWEET_LENGTH and not core.get("quoted_id") and not core.get("retweeted_id")


def get_screen_names(tweet):
    name = "mentioned_screen_name"
    return [mention.get(name) for mention in tweet["user_mentions"] if mention.get(name) in SCREEN_NAMES]


def choose_user_mentions(tweet):
    if not check_if_tweet_is_valid_for_scoring(tweet):
        return
    for screen_name in get_screen_names(tweet):
        if len(SCORING_TWEETS[screen_name]) < MAX_TWEETS_PER_SCREEN_NAME:
            SCORING_TWEETS[screen_name].append(tweet)


def parse_tweets_data():
    tweet_files = get_data_filepaths(RAW_DIR, "stf", ".txt")

    for _file in tweet_files:
        for tweet in load_tweets(_file):
            parse_tweet(tweet)
    
    separate_users_tweets()
    save_parsed_tweets()
    save_chosen_for_scoring()
    
    prefix_files(RAW_DIR, "parsed")


if __name__ == '__main__':
    pass
