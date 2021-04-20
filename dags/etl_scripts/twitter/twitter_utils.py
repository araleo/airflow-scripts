"""
Twitter's utils.
"""

from datetime import datetime
import json

import pandas as pd


def timestamp_to_datetime(ts):
    try:
        _ts = int(ts)
    except TypeError:
        return
    else:
        return datetime.fromtimestamp(_ts / 1000)


def load_tweets(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        try:
            tweets = [json.loads(json.loads(tweet)) for tweet in lines]
        except TypeError:
            tweets = [json.loads(tweet) for tweet in lines]
    return tweets


def build_dataframe(filepath):
    tweets = load_tweets(filepath)
    return pd.DataFrame(tweets)


if __name__ == "__main__":
    pass
