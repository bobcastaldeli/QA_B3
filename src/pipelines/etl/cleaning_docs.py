"""
This module clean documents data for indexing.
"""

# %%
import yaml
import logging
from prepare_data import clean_data


# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %%
with open("conf/catalog.yaml", "r", encoding="utf-8") as f:
    catalog = yaml.safe_load(f)


# %%
docs_df = clean_data(
    path=catalog["intermediate"],
    column="content",
)


docs_df.to_csv(catalog["features"], index=False)
# %%
