from typing import List, Optional

from sqlalchemy import ForeignKey, String, create_engine, select, DateTime, Column, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, joinedload
import uuid
import asyncio

from vector_storage import create_collection, add_data_to_the_collection
from utils import get_content_out_of_file, get_overlapping_chunks

import time
import os

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    collection_name: Mapped[str] = mapped_column(String(256))

    files: Mapped[List['File']] = relationship(
        back_populates = 'project', cascade = "all, delete-orphan"
    )
    requests: Mapped[List['Request']] = relationship(
        back_populates = 'request', cascade = "all, delete-orphan"
    )

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    path: Mapped[str] = mapped_column(String(256))
    content: Mapped[str] = mapped_column(Text)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(
        back_populates = "project"
    )

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(Text)
    limitations: Mapped[str] = mapped_column(Text)

    content: Mapped[str] = mapped_column(Text)
    thinking: Mapped[str] = mapped_column(Text)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(
        back_populates = "project"
    )

def load_engine(
        host = 'database',
        retries = 10,
        delay = 2
):
    for i in range(retries):
        try:
            engine = create_engine(
                f'postgresql+psycopg2://projects_service_user:gH8i9v@{host}/projects_database',
                pool_size = 20,
                max_overflow = 0
            )
            with engine.connect() as conn:
                pass
            Base.metadata.create_all(engine)
            return engine
        except Exception as e:
            print(f"DB is not ready. Retry {i+1}...")
            time.sleep(delay)

    raise Exception('Database connection failed after retries')

def create_project(engine, title):
    with Session(bind = engine) as session:
        while True:
            collection_name = uuid.uuid4()
            if create_collection(collection_name):
                break
        project = Project(
            collection_name = collection_name,
            title = title
        )
        session.add_all([project])
        session.commit()

        return project.collection_name

def get_all_projects(engine):
    with Session(bind = engine) as session:
        stmt = select(Project).order_by(Project.id.desc()).options(
            joinedload(Project.files).joinedload(Project.requests)
        )
        return session.execute(stmt).scalars().all()

def get_project_by_id(engine, id):
    with Session(bind = engine) as session:
        stmt = select(Project).where(Project.id == id).options(
            joinedload(Project.files).joinedload(Project.requests)
        )
        return session.execute(stmt).scalar_one_or_none()

async def save_file(file) -> tuple[str, str] | None:
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)

    original_filename = file.filename or "unnamed"
    unique_name = f"{str(uuid.uuid4()) + "." +original_filename.split(".")[-1]}"
    file_path = os.path.join(upload_dir, unique_name)

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        return (original_filename, file_path)
    except Exception:
        return None
    
async def add_file(engine, qdrant, project_id, file):
    with Session(bind = engine) as session:
        original_filename, file_path = await save_file(file)
        project = get_project_by_id(project_id)
        content = get_content_out_of_file(file_path)
        file_object = File(
            title = original_filename,
            file_path = file_path,
            content = content,
            project = project
        )
        add_data_to_the_collection(
            data = list(get_overlapping_chunks(
                content = content,
                size = 500,
                overlap = 50
            )),
            collection_name = project.collection_name,
            qdrant = qdrant
        )

        session.add_all([file_object])
        session.commit()
    
def add_request_to_the_project(engine, project_id, task, limitations, content, thinking):
    with Session(bind = engine) as session:
        request = Request(
            task = task,
            limitations = limitations,
            content = content,
            thinking = thinking,
            project = get_project_by_id(project_id)
        )

        session.add_all([request])
        session.commit()