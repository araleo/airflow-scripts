"""
G1's package constants
"""

DATA_DIR = "/home/leonardo/no_comments/data"

RAW_DIR = "/home/leonardo/no_comments/data/raw"

TRANSFORMED_DIR = "/home/leonardo/no_comments/data/transformed"

LOADED_DIR = "/home/leonardo/no_comments/data/loaded"

ERROR_LOG_PATH = "/home/leonardo/no_comments/data/errorlog.txt"

HEADERS = ["PAGE", "TITLE", "DESCRIPTION", "DATE", "COMMENTS", "URL", "TIMESTAMP"]

FILTER_COLUMNS = ["ID_PAGINA", "ID_CATEGORIA", "TITLE", "DESCRIPTION", "DATAHORA", "COMMENTS", "URL"]

DB_COLUMNS = ["id_pagina", "id_categoria", "titulo", "descricao", "datahora", "comentarios", "url"]


if __name__ == '__main__':
    pass
