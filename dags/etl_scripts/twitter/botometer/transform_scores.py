"""
Module to transform users botometer scores data
and prepare it to be loaded into a relational DB.
"""

from datetime import datetime

from etl_scripts.global_utils.global_utils import df_to_csv
from etl_scripts.global_utils.global_utils import get_data_filepaths
from etl_scripts.global_utils.global_utils import prefix_file
from etl_scripts.twitter.constants import SCORED_DATA_DIR
from etl_scripts.twitter.constants import SCORES_CSV_DIR
from etl_scripts.twitter.twitter_utils import build_dataframe


def normalize_scores(df):
    columns = ["cap", "astroturf", "fake_follower", "financial", "other", "overall", "self_declared", "spammer"]
    for column in columns:
        df[column] = df[column].apply(lambda x: int(x * 100))
    return df


def transform_scores_data():
    filepaths = get_data_filepaths(SCORED_DATA_DIR, "scored", ".txt")
    for filepath in filepaths:
        df = build_dataframe(filepath)
        df.rename(columns={"user_profile_image_url_https": "user_profile_image_url"}, inplace=True)
        df["scoring_time"] = df.scoring_time.apply(datetime.fromtimestamp)
        df = normalize_scores(df)
        df_to_csv(df, SCORES_CSV_DIR, "scores")
        prefix_file(filepath, "transformed")

        
if __name__ == "__main__":
    pass
