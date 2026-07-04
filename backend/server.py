from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles

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
from agent import load_llm_client, make_request
from utils import project_to_json, projects_to_json
from forms import AddNewProjectForm, AddRequestToTheProjectForm

app = FastAPI()
projects_router = APIRouter(prefix = "/projects")

qdrant = load_qdrant()
engine = load_engine()
client = load_llm_client()

@projects_router.get('/')
def get_all_projects():
    projects = get_all_projects(engine)
    return projects_to_json(projects)

@projects_router.get('/{id}')
def get_project(id: int):
    project = get_project_by_id(engine, id)
    return project_to_json(project)

@projects_router.post('/add')
def add_new_project(form: AddNewProjectForm):
    id = create_project(
        engine = engine,
        title = form.title
    )
    return {"project_id": id}

@projects_router.post('/{id}/add')
def add_request_to_the_project(id: int, form: AddRequestToTheProjectForm):
    project = get_project_by_id(engine = engine, id = id)
    content, thinking = make_request(
        task = form.task,
        limitations = form.limitations,
        collection_name = project.collection_name,
        client = client
    )
    add_request_to_the_project(
        engine = engine,
        project = id,
        task = form.task,
        limitations = form.limitations,
        content = content,
        thinking = thinking
    )
    return {"content": content, "thinking": thinking}

@projects_router.post('/{id}/files/add')
def add_files(id: int, files: List[UploadFile] = File(...)):
    try:
        for file in files:
            add_file(
                engine = engine,
                qdrant = qdrant,
                project_id = id,
                file = file
            )
        return {'response': "Файлы загружены"}
    except Exception as e:
        return {'response': "Произошла ошибка при загрузке одного из файлов", "error": str(e)}
    
app.include_router(projects_router)
app.mount('/files', StaticFiles(directory = 'uploads'), name = 'files')