"""
G1's package constants
"""

DATA_DIR = "/opt/airflow/data/g1"

RAW_DIR = "/opt/airflow/data/g1/raw"

TRANSFORMED_DIR = "/opt/airflow/data/g1/transformed"

LOADED_DIR = "/opt/airflow/data/g1/loaded"

ERROR_LOG_PATH = "/opt/airflow/data/errorlog.txt"

HEADERS = ["PAGE", "TITLE", "DESCRIPTION", "DATE", "COMMENTS", "URL", "TIMESTAMP"]

FILTER_COLUMNS = ["ID_PAGINA", "ID_CATEGORIA", "TITLE", "DESCRIPTION", "DATAHORA", "COMMENTS", "URL"]

DB_COLUMNS = ["id_pagina", "id_categoria", "titulo", "descricao", "datahora", "comentarios", "url"]


if __name__ == '__main__':
    pass
