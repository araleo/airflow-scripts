import os

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

from .Errors import CouldNotInsertException
from .Errors import CouldNotInsertMultipleException


class PostgresConn:

    def __init__(self):
        # "dbname=database user=user password=pwd host=host"
        self.conn = psycopg2.connect(os.environ["PSYCOPG2_CONN_STRING"])
        self.cur = self.conn.cursor()

    def get_id_or_create(self, filter_field, filter_values, fields, schema, table, insert_fields, insert_values):
        res = self.filter(filter_field, filter_values, fields, schema, table)
        if res:
            code = res[0][0]
        else:
            code = self.insert(insert_values, insert_fields, schema, table)
        return code

    def select(self, fields, schema, table):
        query = sql.SQL("select {fields} from {table}").format(
            fields=sql.SQL(",").join(map(sql.Identifier, fields)),
            table=sql.Identifier(schema, table)
        )
        self.cur.execute(query)
        return self.cur.fetchall()

    def filter(self, filter_field, filter_values, fields, schema, table):
        query = sql.SQL("select {fields} from {table} where {filter_field} in %s").format(
            fields=sql.SQL(",").join(map(sql.Identifier, fields)),
            table=sql.Identifier(schema, table),
            filter_field=sql.Identifier(filter_field),
        )
        self.cur.execute(query, (tuple(filter_values),))
        return self.cur.fetchall()

    def insert(self, values, fields, schema, table):
        query = self.build_insert_query(fields, schema, table)
        try:
            self.cur.execute(query, values)
        except psycopg2.Error as e:
            raise CouldNotInsertException
        else:
            self.conn.commit()
            _id = self.cur.fetchall()[0][0]
            return _id

    def build_insert_query(self, fields, schema, table):
        return sql.SQL("insert into {table} ({fields}) values ({values}) returning {ret}").format(
            table=sql.Identifier(schema, table),
            fields=sql.SQL(",").join(map(sql.Identifier, fields)),
            values=sql.SQL(",").join(sql.Placeholder() * len(fields)),
            ret=sql.Identifier("id")
        )

    def insert_multiple(self, fields, values, schema, table):
        query = self.build_insert_multiple_query(fields, schema, table)
        try:
            execute_values(self.cur, query, values)
        except psycopg2.Error:
            raise CouldNotInsertMultipleException
        else:
            self.conn.commit()

    def build_insert_multiple_query(self, fields, schema, table):
        return sql.SQL("insert into {table} ({fields}) values {values}").format(
            table=sql.Identifier(schema, table),
            fields=sql.SQL(",").join(map(sql.Identifier, fields)),
            values=sql.SQL(",").join(sql.Placeholder() * 1)
        )

    def close(self):
        self.cur.close()
        self.conn.close()
