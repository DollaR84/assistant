from db import db_session
from db.models import File


@db_session
def get_files(
        project_id, module_id,
        filename = None,
        all_project_files = False,
        session = None
):
    query = session.query(File)
    query = query.filter(File.project_id == project_id)

    if not all_project_files:
        if module_id:
            query = query.filter(File.module_id == module_id)
        else:
            query = query.filter(File.module_id.is_(None))

    if filename:
        query = query.filter(File.name.contains(filename))

    return query.all()
