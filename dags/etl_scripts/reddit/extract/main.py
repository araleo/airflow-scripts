"""
Main module to gather data from Reddit's API.
"""

from etl_scripts.reddit.extract.constants import SUBS
from etl_scripts.reddit.extract.fetcher import get_subs_posts_data
from etl_scripts.reddit.extract.fetcher import get_token
from etl_scripts.reddit.extract.fetcher import get_user_data
from etl_scripts.reddit.extract.fetcher import load_cred
from etl_scripts.reddit.extract.save import save_data


def extract_reddit_data():
    usr, app = load_cred()
    token = get_token(usr, app)
    headers = {"Authorization": f"bearer {token}", "User-Agent": f"OnlineCounter/1.0 by {usr[0]}"}
    subs_data, posts_data = get_subs_posts_data(headers, SUBS)
    ops_data = [get_user_data(headers, op) for op in set([post["author"] for post in posts_data])]
    save_data(subs_data, posts_data, ops_data)


if __name__ == "__main__":
    pass
