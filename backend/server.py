from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles
import asyncio

from typing import List

from database import (
    load_engine,
    create_project,
    get_project_by_id,
    add_file,
    add_request_to_the_project,
    get_all_projects
)
from vector_storage import load_qdrant
from agent import load_model, make_request
from utils import project_to_json, projects_to_json
from forms import AddNewProjectForm, AddRequestToTheProjectForm

app = FastAPI()
projects_router = APIRouter(prefix = "/projects")

qdrant = load_qdrant()
engine = load_engine()
model = load_model()

@projects_router.get('/')
def list_all_projects():
    projects = get_all_projects(engine)
    return projects_to_json(projects)

@projects_router.get('/{id}')
def list_project_by_id(id: int):
    project = get_project_by_id(
        engine = engine,
        id = id
)
    return project_to_json(project)

@projects_router.post('/add')
def add_new_project(form: AddNewProjectForm):
    id = create_project(
        qdrant = qdrant,
        engine = engine,
        title = form.title,
    )
    return {"project_id": id}

@projects_router.post('/{id}/add')
def add_request_to_the_project_endpoint(id: int, form: AddRequestToTheProjectForm):
    project = get_project_by_id(engine = engine, id = id)
    content = make_request(
        task = form.task,
        limitations = form.limitations,
        collection_name = project.collection_name,
        model = model,
        qdrant = qdrant
    )
    add_request_to_the_project(
        engine = engine,
        project_id = id,
        task = form.task,
        limitations = form.limitations,
        content = content,
    )
    return {"content": content}

@projects_router.post('/{id}/files/add')
def add_files(id: int, files: List[UploadFile] = File(...)):
    try:
        for file in files:
            asyncio.run(add_file(
                engine = engine,
                qdrant = qdrant,
                project_id = id,
                file = file
            ))
        return {'response': "Файлы загружены"}
    except Exception as e:
        print(e)
        return {'response': "Произошла ошибка при загрузке одного из файлов", "error": str(e)}
    
app.include_router(projects_router)
app.mount('/files', StaticFiles(directory = 'uploads'), name = 'files')