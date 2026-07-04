import pymupdf
from docx import Document
import pandas as pd

def get_content_out_of_file(file_path: str) -> str:
    extension = file_path.split('.')[-1].lower()
    if extension == 'pdf':
        doc = pymupdf.open(file_path)
        all_text = ''
        for page in doc:
            all_text += page.get_text() + chr(12)
        return all_text
    elif extension == 'docx':
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        return '\n'.join(full_text)
    elif extension == 'xlsx':
        df = pd.read_excel(file_path, header=None)
        return df.to_string(index=False, header=False)
    else:
        return ''

def project_to_json(project):
    from database import Project
    files = []
    for file in project.files:
        files.append({"id": file.id, "title": file.title})
    project_requests = []
    for request in project.requests:
        project_requests.append({
            'id': request.id,
            "task": request.task,
            "limitations": request.limitations,
            "response": request.content
        })
    return {
        "id": project.id,
        'title': project.title,
        "files": files,
        "requests": project_requests
    }

def projects_to_json(projects):
    return [project_to_json(project) for project in projects]

def get_overlapping_chunks(text, size, overlap):
    if size <= overlap or size <= 0:
        raise ValueError("Размер чанка должен быть больше наложения и больше нуля.")
    
    start = 0
    while start < len(text):
        yield text[start:start + size]
        start += size - overlap
