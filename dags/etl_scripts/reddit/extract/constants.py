"""
Constants
"""

DATA_DIR = "/opt/airflow/data/reddit/raw"

CRED_PATH = "/opt/airflow/dags/etl_scripts/reddit/extract/cred.txt"

SUBS = [
    "brasil",
    "coronabr",
    "desabafos",
    "investimentos",
    "brasilivre",
    "farialimabets",
    "futebol",
]

SUBS_KEYS = [
    "display_name",
    "title",
    "active_user_count",
    "accounts_active",
    "subscribers",
    "id",
]

POSTS_KEYS = [
    "title",
    "subreddit",
    "gilded",
    "total_awards_received",
    "upvote_ratio",
    "created",
    "over_18",
    "num_reports",
    "author",
    "num_comments",
    "id",
    "permalink",
    "stickied",
    "num_crossposts",
    "score",
    "link_flair_text",
]

USERS_KEYS = [
    "is_employee",
    "verified",
    "id",
    "is_gold",
    "has_verified_email",
    "awarder_karma",
    "awardee_karma",
    "total_karma",
    "link_karma",
    "comment_karma",
    "name",
    "created",
    "created_utc",
]


if __name__ == "__main__":
    pass
