"""This module is responsible for scraping data of
the products from the B3 website."""

# %%
import logging
import yaml
import requests
import pandas as pd
from bs4 import BeautifulSoup

# show all text in columns
pd.set_option("display.max_colwidth", None)


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("../../../conf/parameters.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# %%
def product_url(page: str, prefix_url) -> list:
    """This function gets all the urls related
    to products and services of the B3 website.

    parameters
    ----------
    prefixo: str
        prefixo da url
    returns
    list: lista de urls
    """
    response = requests.get(url=page, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    related_url = soup.find_all(
        "a", href=lambda href: href and "produtos" in href
    )
    related_url = [link["href"] for link in related_url]
    # remove any ../ from the url and put the prefixo in the url
    related_url = [s.lstrip("../") for s in related_url]
    # put the prefixo in the url
    related_url = [prefix_url + link for link in related_url]
    return related_url


# %%
def scrap_product_suburl(produtos_url: list, prefix_url: str) -> list:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    list: list of urls
    """
    produtos_negociacao = []
    for produto in produtos_url:
        try:
            response = requests.get(url=produto, timeout=5)
        except:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        # get
        related_url = soup.find_all(
            "a",
            href=lambda href: href
            and ("/negociacao/" or "/operacoes/") in href,
        )
        related_url = [link["href"] for link in related_url]
        # remove any ../ from the url
        related_url = [s.lstrip("../") for s in related_url]
        # put the prefixo in the url
        related_url = [prefix_url + link for link in related_url]
        produtos_negociacao.append(related_url)
        # delete all empty lists
        produtos_negociacao = [x for x in produtos_negociacao if x != []]
    return produtos_negociacao


# %%
def scrap_product_category(produtos_url: list) -> pd.DataFrame:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    df: pandas DataFrame
    """
    dataframe = pd.DataFrame(columns=["product", "product_category"])
    for product in produtos_url:
        # get response only for valid urls
        try:
            response = requests.get(product, timeout=5)
        except:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        # get all the links in sub-nav menu only if it exists
        product_category = soup.find_all("ul", {"class": "sub-nav"})
        if product_category:
            product_category = product_category[0].find_all(
                "a", href=lambda href: href and "produtos" in href
            )
            product_category = [link["href"] for link in product_category]
            # remove any ../ from the url and put the prefixo in the url
            product_category = [s.lstrip("../") for s in product_category]
            # put the prefixo in the url
            product_category = [
                config["prefixo_url"] + link for link in product_category
            ]
            dataframe = dataframe.append(
                pd.DataFrame(
                    {"product": product, "product_category": product_category}
                )
            )
            dataframe.reset_index(drop=True, inplace=True)
            dataframe.drop_duplicates(
                subset=["product_category"], inplace=True
            )
    return dataframe


# %%
def scrap_product_section(produtos_links: pd.DataFrame) -> list:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    df: pandas DataFrame
    """
    product_sections = []
    related_products_list = produtos_links["product_category"].tolist()
    for product in related_products_list:
        try:
            response = requests.get(product)
        except:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        related_sections = soup.find_all("ul", {"class": "side-nav"})
        if related_sections:
            related_sections = related_sections[0].find_all(
                "a", href=lambda href: href and "produtos" in href
            )
            related_sections = [link["href"] for link in related_sections]
            # remove any ../ from the url and put the prefixo in the url
            related_sections = [s.lstrip("../") for s in related_sections]
            # put the prefixo in the url
            related_sections = [
                config["prefixo_url"] + link for link in related_sections
            ]
        else:
            related_sections = [
                product
            ]  # append an empty list when side-nav is not found
        product_sections.append(related_sections)
        product_sections = [
            item for sublist in product_sections for item in product_sections
        ]
    return product_sections


# %%
def scrap_product_description(product_url: list) -> pd.DataFrame:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    df: pandas DataFrame
    """
    products_df = pd.DataFrame(columns=["url", "text"])
    products = product_url
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
