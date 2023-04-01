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
    dataframe[column] = dataframe[column].str.replace("\n", "")
    dataframe[column] = dataframe[column].str.replace("en_USesen_USes", "")

    return dataframe
