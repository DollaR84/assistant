from db import db_session
from db.models import Module


@db_session
def get_modules(project_id, parent_id, all_project_modules = False, session = None):
    query = session.query(Module)
    query = query.filter(Module.project_id == project_id)

    if not all_project_modules:
        if parent_id:
            query = query.filter(Module.parent_id == parent_id)
        else:
            query = query.filter(Module.parent_id.is_(None))

    return query.all()
