from db import db_session
from db.models import Project


@db_session
def create_project(name, path, work_subfolder, session):
    project = Project(
        name=name,
        path=path,
        work_subfolder=work_subfolder,
    )

    session.add(project)
    session.commit()
