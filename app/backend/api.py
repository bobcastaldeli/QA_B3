"""
This module contains the API endpoints for question answering of B3 products and services.
"""

import time
import subprocess
import uvicorn
from fastapi import FastAPI, HTTPException
from haystack.pipelines import Pipeline
from haystack.utils import launch_es


# ELASTICSEARCH_CONTAINER_NAME = "elasticsearch"
# subprocess.run(
#    [f"docker start {ELASTICSEARCH_CONTAINER_NAME}"], shell=True, check=False
# )

ELASTICSEARCH_CONTAINER_NAME = "elasticsearch"


app = FastAPI()


@app.on_event("startup")
async def startup_es():
    """
    This function is responsible for starting the Elasticsearch container.
    """
    subprocess.run(
        [f"docker start {ELASTICSEARCH_CONTAINER_NAME}"],
        shell=True,
        check=False,
    )


# cache the pipeline from yaml file
@app.on_event("startup")
async def load_pipeline():
    """
    This function is responsible for loading the pipeline from the yaml file.
    """
    # Sleep for 60 seconds to allow Elasticsearch to finish initialization

    time.sleep(30)
    app.pipeline = Pipeline.load_from_yaml("conf/pipline.yaml")


@app.on_event("shutdown")
async def shutdown():
    """
    This function is responsible for shutting down the Elasticsearch container.
    """
    subprocess.run(
        [f"docker stop {ELASTICSEARCH_CONTAINER_NAME}"],
        shell=True,
        check=False,
    )


@app.get("/query")
async def get_query(
    query: str,
):
    """
    This endpoint is responsible for answering questions about B3 products and services.
    """
    try:
        result = app.pipeline.run(query=query)
        answer = str(result["answers"][0]).split("answer='")[1].split("',")[0]
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app, host="127.0.0.1", port=8000, log_level="info", reload=True
    )
