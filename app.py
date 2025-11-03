from typing import Union
from fastapi import FastAPI

from search_index import SearchIndex

app = FastAPI()

@app.get("/")
def get_root():
    return {"Hello":"world"}

@app.get("/init")
def init_index():
    index = SearchIndex()
    index.index_text_documents("data")
    
    return {"response":"Text documents have been cleaned"}
    