"""
Module to scrap news from g1's main, RJ and MG pages
"""

from datetime import datetime
import os
import requests

from bs4 import BeautifulSoup

from etl_scripts.g1.constants import RAW_DIR


def get_soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def filter_urls(urls):
    date_str = datetime.now().strftime("%Y/%m/%d")
    filtered = [u for u in urls if u is not None and u.startswith("https://g1.globo.com/") and date_str in u]
    return set(filtered)


def scrap_page(url):
    soup = get_soup(url)
    urls = filter_urls([u.get("href") for u in soup.find_all("a") if u is not None])
    return urls


def remove_semicolon(text):
    while ";" in text:
        text = text.replace(";", "")
    return text


def select_element(soup, selector):
    try:
        element = soup.select(selector)[0].getText().strip()
    except IndexError:
        element = "Null"
    return remove_semicolon(element)


def scrap_article(url):
    soup = get_soup(url)
    page = select_element(soup, ".header-title a")
    title = select_element(soup, ".title h1")
    desc = select_element(soup, ".content-head__subtitle")
    date = select_element(soup, ".content-publication-data__updated time")
    comments = str(bool(soup.select("#boxComentarios")))
    ts = str(datetime.now().timestamp())
    return page, title, desc, date, comments, url, ts


def make_csv(data):
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(RAW_DIR, f"g1_{today}.txt")
    with open(csv_path, "a") as f:
        for row in data:
            f.write(";".join(row))
            f.write("\n")


def g1_scrapper():
    urls_main = scrap_page("https://g1.globo.com/")
    urls_rj = scrap_page("https://g1.globo.com/rj/rio-de-janeiro/")
    urls_mg = scrap_page("https://g1.globo.com/mg/minas-gerais/")
    urls_set = urls_main.union(urls_rj).union(urls_mg)
    data = [scrap_article(url) for url in urls_set]
    make_csv(data)


if __name__ == '__main__':
    pass
