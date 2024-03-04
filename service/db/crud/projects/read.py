from db import db_session
from db.models import Project


@db_session
def get_project(name, session):
    query = session.query(Project)
    query = query.filter(Project.name == name)
    return query.one_or_none()
