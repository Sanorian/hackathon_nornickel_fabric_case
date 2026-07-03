from fastapi import FastAPI

from database import load_engine, create_collection
from vector_storage import load_qdrant
from agent import load_llm_client

app = FastAPI()
qdrant = load_qdrant()
engine = load_engine()
client = load_llm_client()

@app.get('/projects')
def get_all_projects():
    ...

@app.get('/projects/{id}')
def get_project(id: int):
    ...

@app.post('/projects/add')
def add_new_project():
