"""
This module contains the API endpoints for question answering of B3 products and services.
"""

import time
import uvicorn
from fastapi import FastAPI, HTTPException
from haystack.pipelines import Pipeline


app = FastAPI()


# cache the pipeline from yaml file
@app.on_event("startup")
async def load_pipeline():
    """
    This function is responsible for loading the pipeline from the yaml file.
    """
    time.sleep(30)
    app.pipeline = Pipeline.load_from_yaml("conf/pipline.yaml")


@app.get("/query")
async def get_query(
    query: str,
):
    """
    This endpoint is responsible for answering questions about B3 products and services.
    """
    try:
        result = app.pipeline.run(query=query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
#    uvicorn.run(
#        app, host="127.0.0.1", port=8000, log_level="info", reload=True
#    )
