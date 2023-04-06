"""
This module is responsible for creating a QA pipeline with Haystack.
"""


# %%
import os
import time
import yaml
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, EmbeddingRetriever, FARMReader
from haystack.pipelines import Pipeline


# %%
with open("../../../conf/parameters.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


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
bm25_retriever = BM25Retriever(document_store=document_store)


# %%
reader = FARMReader(model_name_or_path=config["reader_model"], use_gpu=True)


# %%
pipeline = Pipeline()
pipeline.add_node(
    component=bm25_retriever, name="BM25Retriever", inputs=["Query"]
)
pipeline.add_node(
    component=reader, name="FARMReader", inputs=["BM25Retriever"]
)


# %%
pipeline.save_to_yaml("../conf/pipline.yaml")
