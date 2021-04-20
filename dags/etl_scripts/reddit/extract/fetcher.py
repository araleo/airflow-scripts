"""
Tools to access and gather data from Reddit's API.
"""

from datetime import datetime

import requests
import requests.auth

from etl_scripts.reddit.extract.constants import CRED_PATH
from etl_scripts.reddit.extract.constants import POSTS_KEYS
from etl_scripts.reddit.extract.constants import SUBS_KEYS
from etl_scripts.reddit.extract.constants import USERS_KEYS


def load_cred():
    with open(CRED_PATH, "r") as f:
        usr, app = f.readline().split(), f.readline().split()
    return usr, app


def get_token(usr, app):
    client_auth = requests.auth.HTTPBasicAuth(app[0], app[1])
    post_data = {"grant_type": "password", "username": usr[0], "password": usr[1]}
    headers = {"User-Agent": f"OnlineCounter/1.0 by {usr[0]}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()["access_token"]


def append_time(data):
    now = datetime.now()
    day_hour = now.strftime("%d/%m/%Y %H:%M")
    day, hour = day_hour.split()
    data["day"] = day
    data["hour"] = hour
    data["timestamp"] = str(now.timestamp())
    return data


def get_sub_data(headers, subname):
    response = requests.get(f"https://oauth.reddit.com/r/{subname}/about", headers=headers)
    sub = response.json()["data"]
    data = {k: str(sub[k]) for k in sub if k in SUBS_KEYS}
    return append_time(data)


def get_top_posts_data(headers, subname, num_posts):
    response = requests.get(f"https://oauth.reddit.com/r/{subname}/top/?t=day.json", headers=headers)
    data = response.json()["data"]
    posts = []
    for i in range(num_posts):
        d = data["children"][i]["data"]
        _data = {k: str(d[k]) for k in d if k in POSTS_KEYS}
        _data["rank"] = str(i + 1)
        posts.append(append_time(_data))
    return posts


def get_user_data(headers, username):
    response = requests.get(f"https://oauth.reddit.com/user/{username}/about", headers=headers)
    data = response.json()["data"]
    user = {k: str(data[k]) for k in data if k in USERS_KEYS}
    user["description"] = data["subreddit"]["public_description"]
    return append_time(user)


def get_subs_posts_data(headers, subs):
    subs_data = []
    posts_data = []
    for sub in subs:
        subs_data.append(get_sub_data(headers, sub))
        posts_data.extend(get_top_posts_data(headers, sub, 3))
    return subs_data, posts_data


if __name__ == "__main__":
    pass
