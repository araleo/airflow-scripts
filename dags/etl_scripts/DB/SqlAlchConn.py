from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from etl_scripts.DB.constants import SQL_ALCH_CONN_STRING


class SqlAlchConn:

    def __init__(self):
        self.engine = self.open()

    def load(self, df, table, schema):
        try:
            df.to_sql(name=table, con=self.engine, schema=schema, if_exists="append", index=False, method=None)
        except IntegrityError:
            raise IntegrityError
        except AttributeError:
            raise AttributeError
        finally:
            self.engine.dispose()

    def close(self):
        self.engine.dispose()

    def open(self):
        # "postgresql://user:pwd@host:port/database"
        return create_engine(SQL_ALCH_CONN_STRING)
