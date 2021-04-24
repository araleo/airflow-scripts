"""
Module to go through tweets separated to be scored,
call the botometer api scoring it's users and save
the parsed tweets + users + scores into a txt file.
"""

from datetime import datetime
import os
import ntpath

from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_file
from etl_scripts.twitter.botometer.query_api import query_botometer
from etl_scripts.twitter.constants import SCORED_DATA_DIR
from etl_scripts.twitter.constants import SCORING_DATA_DIR
from etl_scripts.twitter.twitter_utils import load_tweets
from etl_scripts.twitter.twitter_utils import save_file


PARSED_TWEETS = []


def save_scored_tweets():
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    scored_path = os.path.join(SCORED_DATA_DIR, f"scored_{now}.txt")
    save_file(scored_path, PARSED_TWEETS)


def parse_tweet(tweet, scores, mentioned_user, scoring_time):
    raw_scores = scores["raw_scores"]["universal"]
    filtered = dict()
    filtered["tweet_id"] = tweet["tweet_core"].get("id")
    filtered["text"] = tweet["tweet_core"].get("text")
    filtered["mentioned_user"] = mentioned_user
    filtered["created_at"] = tweet["tweet_core"].get("created_at")
    filtered["user_screen_name"] = tweet["user_core"].get("user_screen_name")
    filtered["user_profile_image_url_https"] = tweet["user_core"].get("user_profile_image_url_https")
    filtered["cap"] = scores["cap"].get("universal")
    filtered["astroturf"] = raw_scores.get("astroturf")
    filtered["fake_follower"] = raw_scores.get("fake_follower")
    filtered["financial"] = raw_scores.get("financial")
    filtered["other"] = raw_scores.get("other")
    filtered["overall"] = raw_scores.get("overall")
    filtered["self_declared"] = raw_scores.get("self_declared")
    filtered["spammer"] = raw_scores.get("spammer")
    filtered["scoring_time"] = scoring_time
    return filtered


def parse_scores(tweets, users_scores, mentioned_screen_name):
    scoring_time = datetime.now().timestamp()
    for tweet in tweets:
        user_scores = users_scores.get(tweet["user_core"].get("user_screen_name"))
        if user_scores.get("raw_scores"):
            PARSED_TWEETS.append(parse_tweet(tweet, user_scores, mentioned_screen_name, scoring_time))


def get_mentioned_from_filename(filepath):
    basename = ntpath.basename(filepath)
    splited = basename.split("_")
    name_parts = splited[1:-1]
    return "_".join(name_parts)


def score_users():
    for filepath in get_data_filepaths(SCORING_DATA_DIR, "score", ".txt"):
        mentioned_screen_name = get_mentioned_from_filename(filepath)
        tweets = load_tweets(filepath)
        users_screen_names = set(tweet["user_core"].get("user_screen_name") for tweet in tweets)
        users_scores = query_botometer(users_screen_names)
        parse_scores(tweets, users_scores, mentioned_screen_name)
        prefix_file(filepath, "parsed")
    save_scored_tweets()


if __name__ == "__main__":
    pass
