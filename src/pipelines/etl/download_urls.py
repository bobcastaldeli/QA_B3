"""
This module downloads all the urls related
to products and services of the B3 website.
"""


# %%
import yaml
import logging
import pandas as pd
from scrap_data import (
    product_url,
    scrap_product_suburl,
    scrap_product_category,
)


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("../../../conf/parameters.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# %%
produtos_url = product_url(config["produtos_page"], config["prefixo_url"])


# %%
produtos_negociacao = scrap_product_suburl(produtos_url, config["prefixo_url"])
produtos_negociacao = [
    item for sublist in produtos_negociacao for item in sublist
]


# %%
categoria_produtos = scrap_product_category(produtos_url)


# %%
categoria_produtos_negociacao = scrap_product_category(produtos_negociacao)


# %%
# concat both dataframes
categoria_produtos = pd.concat(
    [categoria_produtos, categoria_produtos_negociacao], ignore_index=True
)


# %%
categoria_produtos.to_csv(
    "../../../data/01_raw/categoria_produtos.csv",
)
