"""This module is responsible for scraping data of the products from the B3
website."""

# %%
import logging
import yaml
import requests
import pandas as pd
from bs4 import BeautifulSoup


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# %%
def srap_cat_produtos(produtos: str, prefixo: str, sufixo: str) -> list:
    """This function gets all the urls related to products and services in
    negociation.

    Parameters
    ----------
    produtos: str
        url of the products and services page
    prefixo: str
        prefix of the url
    sufixo: str
        sufix of the url
    returns
    list: list of urls
    """
    response = requests.get(produtos)
    soup = BeautifulSoup(response.text, "html.parser")
    related_links = soup.find_all(
        "a", href=lambda href: href and sufixo in href
    )
    links = [
        link.replace("../..", prefixo)
        for link in [link["href"] for link in related_links]
    ]
    return links


# make a loop to get all the links of each product
def scrap_subcat_produtos(links: list, produtos: str, prefixo: str) -> list:
    """This function gets all the urls related to products and services in
    negociation.

    Parameters
    ----------
    links: list
        list of urls
    produtos: str
        url of the products and services page
    prefixo: str
        prefix of the url
    returns
    list: list of urls
    """
    product_links = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        related_products_links = soup.find_all(
            "a", href=lambda href: href and produtos in href
        )
        product_links.append(
            [
                link.replace(["../../", ""])
                for link in [link["href"] for link in related_products_links]
            ]
        )
        products = [
            [prefixo + element for element in sub_list]
            for sub_list in product_links
        ]
        products = [item for sublist in products for item in sublist]
    return products


# %%
# transform the list of lists into a list
# scrap all the text from each product than save into a dataframe with url and text
def scrap_ficha_produto(products: list) -> pd.DataFrame:
    """This function scrapes all the text from each product than save into a
    dataframe with url and text.

    Parameters
    ----------
    products: list
        list of urls
    returns
    pd.DataFrame: dataframe with url and text
    """
    products_df = pd.DataFrame(columns=["url", "text"])
    for product in products:
        response = requests.get(product)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.find_all("li")
        text = [element.text for element in text]
        text = " ".join(text)
        products_df = products_df.append(
            {"url": product, "text": text}, ignore_index=True
        )
    return products_df
