"""
This module write data to a Elastic Search document store.
"""


# %%
import os
import time
import yaml
import logging
import pandas as pd
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import launch_es
from prepare_data import write_data


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("conf/catalog.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# %%
launch_es()


# %%
time.sleep(30)


# %%
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document",
)


# %%
docs_df = pd.read_csv(config["features"])


# %%
write_data(docs_df, document_store)
