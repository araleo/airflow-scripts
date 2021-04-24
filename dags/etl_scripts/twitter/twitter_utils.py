"""
Twitter's utils.
"""

from datetime import datetime
import json

import pandas as pd


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
