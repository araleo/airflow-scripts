"""
Module to unpack a tweet json into a filtered dictionary
according to the project's bussiness rules
"""


def filter_tweet(tweet):
    filtered = dict()
    filtered["tweet_core"] = extract_tweet_core(tweet)
    filtered["tweet_counts"] = extract_tweet_counts(tweet)
    filtered["user_core"] = extract_user_core(tweet)
    filtered["user_mentions"] = extract_user_mentions(tweet)
    filtered["urls"] = extract_urls(tweet)
    filtered["hashtags"] = extract_hashtags(tweet)
    filtered["medias"] = extract_medias(tweet)
    return filtered


def extract_tweet_core(tweet):
    filtered = dict()
    filtered["id"] = tweet.get("id")
    filtered["created_at"] = tweet.get("created_at")
    filtered["text"] = tweet.get("text") if not tweet.get("truncated") else tweet["extended_tweet"].get("full_text")
    filtered["source"] = tweet.get("source")
    filtered["in_reply_to_status_id"] = tweet.get("in_reply_to_status_id")
    filtered["in_reply_to_user_id"] = tweet.get("in_reply_to_user_id")
    filtered["in_reply_to_screen_name"] = tweet.get("in_reply_to_screen_name")
    filtered["geo"] = tweet.get("geo")
    filtered["coordinates"] = tweet.get("coordinates")
    filtered["place"] = tweet.get("place")
    filtered["user_twitter_id"] = tweet["user"].get("id")
    filtered["timestamp_ms"] = tweet.get("timestamp_ms")
    filtered["quoted_id"] = tweet.get("quoted_status").get("id") if tweet.get("quoted_status") else None
    filtered["retweeted_id"] = tweet.get("retweeted_status").get("id") if tweet.get("retweeted_status") else None
    return filtered


def extract_tweet_counts(tweet):
    filtered = dict()
    filtered["tweet_id"] = tweet.get("id")
    filtered["tweet_quote_count"] = tweet.get("quote_count")
    filtered["tweet_reply_count"] = tweet.get("reply_count")
    filtered["tweet_retweet_count"] = tweet.get("retweet_count")
    filtered["tweet_favorite_count"] = tweet.get("favorite_count")
    return filtered


def extract_user_core(tweet):
    filtered = dict()
    filtered["user_id"] = tweet["user"].get("id")
    filtered["user_name"] = tweet["user"].get("name")
    filtered["user_screen_name"] = tweet["user"].get("screen_name")
    filtered["user_followers_count"] = tweet["user"].get("followers_count")
    filtered["user_friends_count"] = tweet["user"].get("friends_count")
    filtered["user_statuses_count"] = tweet["user"].get("statuses_count")
    filtered["user_location"] = tweet["user"].get("location")
    filtered["user_url"] = tweet["user"].get("url")
    filtered["user_description"] = "".join(('"', tweet["user"].get("description"), '"')) if tweet["user"].get("description") else None
    filtered["user_created_at"] = tweet["user"].get("created_at")
    filtered["user_geo_enabled"] = tweet["user"].get("geo_enabled")
    filtered["user_profile_image_url_https"] = tweet["user"].get("profile_image_url_https")
    filtered["user_profile_banner_url"] = tweet["user"].get("profile_banner_url")
    return filtered


def extract_user_mentions(tweet):
    mentions = []
    for mention in tweet["entities"].get("user_mentions", []):
        filtered = dict()
        filtered["tweet_id"] = tweet.get("id")
        filtered["mentioned_screen_name"] = mention.get("screen_name")
        filtered["mentioned_name"] = mention.get("name")
        filtered["mentioned_id"] = mention.get("id")
        filtered["mentioned_begins_index"] = mention.get("indices")[0]
        filtered["mentioned_ends_index"] = mention.get("indices")[1]
        mentions.append(filtered)
    return mentions


def extract_urls(tweet):
    urls = []
    for url in tweet["entities"].get("urls", []):
        filtered = dict()
        filtered["tweet_id"] = tweet.get("id")
        filtered["url"] = url.get("url")
        filtered["expanded_url"] = url.get("expanded_url")
        filtered["url_begins_index"] = url.get("indices")[0]
        filtered["url_ends_index"] = url.get("indices")[1]
        urls.append(filtered)
    return urls


def extract_hashtags(tweet):
    hashtags = []
    for hashtag in tweet["entities"].get("hashtags", []):
        filtered = dict()
        filtered["tweet_id"] = tweet.get("id")
        filtered["hashtag_text"] = hashtag.get("text")
        filtered["hashtag_begins_index"] = hashtag.get("indices")[0]
        filtered["hashtag_ends_index"] = hashtag.get("indices")[1]
        hashtags.append(filtered)
    return hashtags


def extract_medias(tweet):
    medias = []
    for media in tweet["entities"].get("medias", []):
        filtered = dict()
        filtered["tweet_id"] = tweet.get("id")
        filtered["media_id"] = media.get("id")
        filtered["media_url"] = media.get("media_url_https")
        filtered["media_type"] = media.get("type")
    return medias


if __name__ == '__main__':
    pass
