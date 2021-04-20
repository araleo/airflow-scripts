"""
Global utils shared between all projects
"""

from datetime import datetime
import ntpath
import os

from sqlalchemy.exc import IntegrityError
import pandas as pd

from etl_scripts.DB.Errors import SQLAlchError
from etl_scripts.DB.SqlAlchConn import SqlAlchConn


def sqlalch_load(df, schema, table, error_list):
    alch = SqlAlchConn()
    try:
        alch.load(df, table, schema)
    except (IntegrityError, AttributeError, ValueError) as e:
        error_list.append(e)
        raise SQLAlchError


def df_to_csv(df, folder, prefix):
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    fp = os.path.join(folder, f"{prefix}_{now}.csv")
    df.to_csv(fp, sep=";", index=False)


def log_errors(filepath, module, errors):
    if errors:
        now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        with open(filepath, "a") as f:
            for e in errors:
                output = "\n".join((now, module, str(e)))
                f.write(output + "\n")


def add_prefix_to_files(folder, old_prefix, new_prefix):
    filepaths = [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith(old_prefix)]
    renamed = [os.path.join(folder, f"{new_prefix}_{ntpath.basename(f)}") for f in filepaths]
    for old_name, new_name in zip(filepaths, renamed):
        os.rename(old_name, new_name)


def prefix_files(folder, prefix):
    filepaths = [os.path.join(folder, f) for f in os.listdir(folder) if not f.startswith(prefix)]
    renamed = [os.path.join(folder, f"{prefix}_{ntpath.basename(f)}") for f in filepaths]
    for old_name, new_name in zip(filepaths, renamed):
        os.rename(old_name, new_name)


def prefix_file(filepath, prefix):
    new_name = os.path.join(ntpath.dirname(filepath), f"{prefix}_{ntpath.basename(filepath)}")
    os.rename(filepath, new_name)


def get_data_filepaths(folder, prefix, suffix):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith(prefix) and f.endswith(suffix)]


def load_dataframes(folder, prefix, suffix, headers=None):
    filepaths = get_data_filepaths(folder, prefix, suffix)
    if not filepaths:
        return None

    if headers is None:
        df = pd.concat((pd.read_csv(f, sep=";") for f in filepaths))
    else:
        df = pd.concat((pd.read_csv(f, sep=";", names=headers) for f in filepaths))

    return df


if __name__ == '__main__':
    pass
