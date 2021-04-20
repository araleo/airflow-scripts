"""
Saves data into csv files.
"""

from datetime import datetime
import os

from etl_scripts.reddit.extract.constants import DATA_DIR


def order_sub_data(sd):
    return (
        sd["display_name"],
        sd["title"],
        sd["subscribers"],
        sd["active_user_count"],
        sd["accounts_active"],
        sd["day"],
        sd["hour"],
        sd["timestamp"],
    )


def order_post_data(pd):
    return (
        pd["subreddit"],
        pd["author"],
        remove_semicolon(pd["title"]),
        remove_semicolon(pd["link_flair_text"]),
        pd["score"],
        pd["upvote_ratio"],
        pd["num_comments"],
        pd["rank"],
        pd["gilded"],
        pd["total_awards_received"],
        pd["num_crossposts"],
        pd["num_reports"],
        pd["over_18"],
        pd["stickied"],
        pd["created"],
        pd["permalink"],
        pd["id"],
        pd["day"],
        pd["hour"],
        pd["timestamp"],
    )


def order_user_data(ud):
    return (
        ud["name"],
        ud["id"],
        remove_semicolon(ud["description"]),
        ud["created"],
        ud["created_utc"],
        ud["verified"],
        ud["has_verified_email"],
        ud["is_employee"],
        ud["total_karma"],
        ud["awarder_karma"],
        ud["awardee_karma"],
        ud["link_karma"],
        ud["comment_karma"],
        ud["is_gold"],
        ud["day"],
        ud["hour"],
        ud["timestamp"],
    )


def remove_semicolon(text):
    while ";" in text:
        text = text.replace(";", " ")
    while "\n" in text:
        text = text.replace("\n", " ")
    return text


def make_csv(data, filepath):
    with open(filepath, "a") as f:
        f.write(";".join(data))
        f.write("\n")


def save_data(subs_data, posts_data, users_data):
    today = datetime.now().strftime("%Y-%m-%d")
    for sd in subs_data:
        make_csv(order_sub_data(sd), os.path.join(DATA_DIR, "subs", f"redditSubsLogs{today}.txt"))
    for pd in posts_data:
        make_csv(order_post_data(pd), os.path.join(DATA_DIR, "posts", f"redditPostsLogs{today}.txt"))
    for ud in users_data:
        make_csv(order_user_data(ud), os.path.join(DATA_DIR, "users", f"redditUsersLogs{today}.txt"))


if __name__ == "__main__":
    pass
