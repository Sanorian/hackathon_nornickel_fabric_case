from pydantic import BaseModel

class AddNewProjectForm(BaseModel):
    title: str

class AddRequestToTheProjectForm(BaseModel):
    task: str
    limitations: str