
ERROR_LOG_PATH = "/home/leonardo/twitter_stf/data/errorlog.txt"

PRO_DIR = "/home/leonardo/twitter_stf/data/processed"

RAW_DIR = "/home/leonardo/twitter_stf/data/raw"

ENTITIES_DATA_DIR = "/home/leonardo/twitter_stf/data/entities"

ENTITIES_CSV_DIR = "/home/leonardo/twitter_stf/data/csvs/entities"

TWEET_DATA_DIR = "/home/leonardo/twitter_stf/data/tweets"

TWEET_CSV_DIR = "/home/leonardo/twitter_stf/data/csvs/tweets"

USER_DATA_DIR = "/home/leonardo/twitter_stf/data/users"

USER_CSV_DIR = "/home/leonardo/twitter_stf/data/csvs/users"

COUNT_COLS_DICT = {
    "tweet_quote_count": "quote_count",
    "tweet_reply_count": "reply_count",
    "tweet_retweet_count": "retweet_count",
    "tweet_favorite_count": "favorite_count"
}

HASHTAG_COLS_DICT = {
    "hashtag_text": "text",
    "hashtag_begins_index": "begin_index",
    "hashtag_ends_index": "end_index"
}

MENTION_COLS_DICT = {
    "mentioned_screen_name": "screen_name",
    "mentioned_name": "name",
    "mentioned_begins_index": "begin_index",
    "mentioned_ends_index": "end_index"
}

URL_COLS_DICT = {
    "url_begins_index": "begin_index",
    "url_ends_index": "end_index"
}

MEDIA_COLS_DICT = {
    "media_id": "twitter_id",
    "media_url": "url",
    "media_type": "type",
    "url_begins_index": "begin_index",
    "url_ends_index": "end_index"
}

USER_COLS_DICT = {
    "user_id": "twitter_id",
    "user_name": "name",
    "user_screen_name": "screen_name",
    "user_followers_count": "followers_count",
    "user_friends_count": "friends_count",
    "user_statuses_count": "statuses_count",
    "user_location": "location",
    "user_url": "url",
    "user_description": "description",
    "user_created_at": "created_at",
    "user_geo_enabled": "geo_enabled",
    "user_profile_image_url_https": "profile_image_url",
    "user_profile_banner_url": "profile_banner_url",
    "collection_time_ts_ms": "collection_time"
}


if __name__ == "__main__":
    pass