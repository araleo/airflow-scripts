"""
Module to query the botometer API.
"""

import botometer

from etl_scripts.twitter.botometer.constants import CRED_PATH

def load_cred():
    with open(CRED_PATH) as f:
        content = f.read()
    creds = content.split()
    api_key = creds[0]
    twitter_keys = creds[1:]
    return api_key, twitter_keys


def build_twitter_auth(twitter_keys_values):
    twitter_keys = ["consumer_key", "consumer_secret", "access_token", "access_token_secret"]
    return dict(zip(twitter_keys, twitter_keys_values))


def query_botometer(users_screen_names):
    api_key, twitter_keys = load_cred()
    twitter_app_auth = build_twitter_auth(twitter_keys)
    bom = botometer.Botometer(wait_on_ratelimit=False, rapidapi_key=api_key, **twitter_app_auth)
    scores = dict(bom.check_accounts_in(users_screen_names))
    return scores


if __name__ == "__main__":
    pass
