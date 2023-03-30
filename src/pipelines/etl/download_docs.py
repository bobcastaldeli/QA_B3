"""
This module is responsible for downloading
all text data related to products and services
of the B3 website.
"""


# %%
import yaml
import logging
import pandas as pd
from scrap_data import (
    scrap_product_section,
    scrap_product_description,
)


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("../../../conf/parameters.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# %%
produtos_url = pd.read_csv(
    "../../../data/01_raw/categoria_produtos.csv", index_col=0
)


# %%
produtos_url = scrap_product_section(
    produtos_url,
)
produtos_url = [item for sublist in produtos_url for item in sublist]


# %%
docs_df = scrap_product_description(
    produtos_url,
)


# %%
docs_df.to_csv(
    "../../../data/02_intermediate/docs.csv",
    index=False,
)

# %%
