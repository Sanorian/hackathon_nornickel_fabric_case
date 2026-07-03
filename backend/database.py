from typing import List, Optional

from sqlalchemy import ForeignKey, String, create_engine, select, DateTime, Column, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, joinedload
import uuid
from vector_storage import create_collection

import time
import os

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    collection_name: Mapped[str] = mapped_column(String(256))

    files = Mapped[List['File']] = relationship(
        back_populates = 'project', cascade = "all, delete-orphan"
    )
    requests = Mapped[List['Request']] = relationship(
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

def create_project(engine):
    with Session(bind = engine) as session:
        while True:
            collection_name = uuid.uuid4()
            if create_collection(collection_name):
                break
        project = Project(
            collection_name = collection_name
        )
        session.add_all([project])
        session.commit()

        return project.collection_name

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
        return (unique_name, file_path)
    except Exception:
        return None