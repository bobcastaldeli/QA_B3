"""
This module write data to a FAISS document store.
"""


import logging
import pandas as pd


logging.basicConfig(
    format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
)
logging.getLogger("haystack").setLevel(logging.INFO)


def clean_data(path: str, column: str) -> pd.DataFrame:
    """
    Clean data for indexing.

    Parameters
    ----------
    path: str
        Path to data.
    column: str
        Column to clean.
    """

    dataframe = pd.read_csv(path)
    dataframe[column] = dataframe[column].str.replace("\n", " ")

    return dataframe


def write_data(dataframe: pd.DataFrame, document_store) -> None:
    """
    Write data to a Elasticsearch document store.

    Parameters
    ----------
    dataframe: pd.DataFrame
        Dataframe to write.
    document_store: ElasticsearchDocumentStore
        Document store to write to.
    """

    for i, row in dataframe.iterrows():
        content = row["content"]
        metadata = {"url": row["url"]}
        document_store.write_documents(
            [{"content": content, "meta": metadata}]
        )
