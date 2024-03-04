from db import db_session
from db.models import Import


@db_session
def get_imports(file_id, module_name = None, session = None):
    query = session.query(Import)
    query = query.filter(Import.file_id == file_id)

    if module_name:
        query = query.filter(Import.module == module_name)

    return query.all()
