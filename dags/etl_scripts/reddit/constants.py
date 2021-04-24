
# Global

DATA_DIR = "/opt/airflow/data/reddit"

CSV_PREFIX = "reddit"

CSV_SUFFIX = ".txt"

ERROR_LOG_PATH = "/opt/airflow/data/reddit/errorlog.txt"


# Subs

SUBS_RAW_DIR = "/opt/airflow/data/reddit/raw/subs"

SUBS_TRANSFORMED_DIR = "/opt/airflow/data/reddit/transformed/subs"

SUBS_HEADERS = [
    "DISPLAY_NAME", "TITLE", "SUBSCRIBERS", "ACTIVE_USER_COUNT", "ACCOUNTS_ACTIVE", "DAY", "HOUR", "TIMESTAMP"
]

SUBS_FILTER_COLUMNS = ["ID_SUB", "ACTIVE_USER_COUNT", "ACCOUNTS_ACTIVE", "SUBSCRIBERS", "COLLECTION_TIME"]


# Users

USERS_RAW_DIR = "/opt/airflow/data/reddit/raw/users"

USERS_TRANSFORMED_DIR = "/opt/airflow/data/reddit/transformed/users"

USERS_HEADERS = [
    "NAME", "ID", "DESCRIPTION", "CREATED", "CREATED_UTC", "VERIFIED",
    "HAS_VERIFIED_EMAIL", "IS_EMPLOYEE", "TOTAL_KARMA", "AWARDER_KARMA",
    "AWARDEE_KARMA", "LINK_KARMA", "COMMENT_KARMA", "IS_GOLD", "DAY", "HOUR", "TIMESTAMP"
]

USERS_FILTER_COLUMNS = ["ID", "NAME", "DESCRIPTION", "CREATED_TS", "VERIFIED", "HAS_VERIFIED_EMAIL", "IS_EMPLOYEE"]

USERS_DB_COLUMNS = ["reddit_id", "name", "description", "created", "verified", "has_verified_email", "is_employee"]

USER_STATS_FILTER_COLUMNS = [
    "ID_BANCO", "TOTAL_KARMA", "LINK_KARMA", "COMMENT_KARMA", "AWARDER_KARMA",
    "AWARDEE_KARMA", "IS_GOLD", "COLLECTION_TIME"
]

USER_STATS_DB_COLUMNS = [
    "id_user", "total_karma", "link_karma", "comment_karma", "awarder_karma",
    "awardee_karma", "is_gold", "collection_time"
]


# Posts

POSTS_RAW_DIR = "/opt/airflow/data/reddit/raw/posts"

POSTS_TRANSFORMED_DIR = "/opt/airflow/data/reddit/transformed/posts"

POSTS_HEADERS = [
    "SUBREDDIT", "AUTHOR", "TITLE", "LINK_FLAIR_TEXT", "SCORE", "UPVOTE_RATIO", "NUM_COMMENTS", "RANK",
    "GILDED", "TOTAL_AWARDS_RECEIVED", "NUM_CROSSPOSTS", "NUM_REPORTS", "OVER_18", "STICKIED", "CREATED",
    "PERMALINK", "ID", "DAY", "HOUR", "TIMESTAMP"
]

POSTS_FILTER_COLUMNS = [
    "ID_SUB", "ID_USER", "ID", "TITLE", "LINK_FLAIR_TEXT", "SCORE", "UPVOTE_RATIO", "NUM_COMMENTS", "GILDED_BOOL",
    "TOTAL_AWARDS_RECEIVED", "NUM_CROSSPOSTS", "OVER_18", "STICKIED", "CREATED_TS", "PERMALINK", "COLLECTION_TIME"
]

POSTS_DB_COLUMNS = [
    "id_sub", "id_user", "reddit_post_id", "title", "flair", "score", "upvote_ratio", "num_comments", "gilded",
    "total_awards_received", "num_crossposts", "over_18", "stickied", "created", "permalink", "collection_time"
]


if __name__ == '__main__':
    pass
