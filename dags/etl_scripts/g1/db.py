from etl_scripts.DB.PostgresConn import PostgresConn


def query_page_id_or_create(page):
    db = PostgresConn()
    res = db.get_id_or_create(
        filter_field="nome",
        filter_values=[page],
        fields=["id", "nome"],
        schema="noticias",
        table="paginas",
        insert_fields=["nome"],
        insert_values=[page]
    )
    return res


def query_page_id(page):
    db = PostgresConn()
    res = db.filter(
        filter_field="nome",
        filter_values=[page],
        fields=["id", "nome"],
        schema="noticias",
        table="paginas"
    )
    db.close()
    return res[0][0]


def query_categories_ids(categories):
    db = PostgresConn()
    res = db.filter(
        filter_field="categoria",
        filter_values=categories,
        fields=["id", "categoria"],
        schema="noticias",
        table="categorias"
    )
    db.close()
    return res


def insert_new_categories(categories):
    cats = [(cat,) for cat in categories]
    db = PostgresConn()
    db.insert_multiple(
        fields=["categoria"],
        values=cats,
        schema="noticias",
        table="categorias"
    )
    db.close()


def select_all_urls():
    db = PostgresConn()
    res = db.select(["url"], "noticias", "noticias")
    db.close()
    return set(url[0] for url in res)


if __name__ == "__main__":
    pass
