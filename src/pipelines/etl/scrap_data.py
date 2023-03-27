"""This module is responsible for scraping data of the products from the B3
website."""

# %%
import time
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
def produto_url(prefix: str) -> list:
    """This function gets all the urls related
    to products and services of the B3 website.

    parameters
    ----------
    prefixo: str
        prefixo da url
    returns
    list: lista de urls
    """
    response = requests.get(url=prefix, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    related_url = soup.find_all(
        "a", href=lambda href: href and "produtos" in href
    )
    related_url = [link["href"] for link in related_url]
    related_url = [
        link.replace("../../pt_br/produtos-e-servicos/", prefix)
        for link in related_url
    ]
    return related_url


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
            product_category = [
                link.replace("../../../../../", config["prefixo_url"])
                for link in product_category
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
def scrap_related_product(produtos_url: list) -> pd.DataFrame:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    df: pandas DataFrame
    """
    dataframe = pd.DataFrame(columns=["product", "related_product"])
    for product in produtos_url:
        # get response only for valid urls
        try:
            response = requests.get(product)
        except:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        # get all the links in sub-nav menu only if it exists
        related_products = soup.find_all("ul", {"class": "sub-nav"})
        if related_products:
            related_products = related_products[0].find_all(
                "a", href=lambda href: href and "produtos" in href
            )
            related_products = [link["href"] for link in related_products]
            related_products = [
                link.replace("../../../../../", config["prefixo_url"])
                for link in related_products
            ]
            dataframe = dataframe.append(
                pd.DataFrame(
                    {"product": product, "related_product": related_products}
                )
            )
            # dataframe.reset_index(drop=True, inplace=True)
            # dataframe.drop_duplicates(inplace=True)
    return dataframe


# %%
def scrap_product_section(produtos_url: list) -> pd.DataFrame:
    """This function gets all the related products of each product in the
    products and services page of the B3 website.

    Parameters
    ----------
    produtos_links: list
        list of urls
    returns
    df: pandas DataFrame
    """
    dataframe = pd.DataFrame(columns=["product", "product_section"])
    related_products_list = produtos_url["product_category"].tolist()
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
            related_sections = [
                link.replace("../../../../../", config["prefixo_url"])
                for link in related_sections
            ]
            dataframe = dataframe.append(
                pd.DataFrame(
                    {"product": product, "product_section": related_sections}
                )
            )
            # dataframe.reset_index(drop=True, inplace=True)
            # dataframe.drop_duplicates(inplace=True)
    return dataframe


# %%
def scrap_product_data(product_url: pd.DataFrame) -> pd.DataFrame:
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
    products = product_url["related_product_section"].tolist()
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


# %%
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
