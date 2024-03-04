import logging

from db import db_session
from db.models import Class, File, Function, Import, Module, Project

from . import data as data_models

from .results import ResultCountAdd, ResultCountUpdate, ResultCountDelete


class DataSaver:

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project: Project = None

        self.added = ResultCountAdd()
        self.updated = ResultCountUpdate()
        self.deleted = ResultCountDelete()

        self.logger = logging.getLogger("debugger")

    def set_project(self, project: Project):
        self.project = project

    def get_object(self, object_cls, all_objects: bool = False, **kwargs):
        session = kwargs.pop("session", None)
        if not session:
            return None

        query = session.query(object_cls)
        for key, value in kwargs.items():
            query = query.filter(getattr(object_cls, key) == value)

        return query.all() if all_objects else query.one_or_none()

    def delete_objects(self, object_cls, **kwargs):
        session = kwargs.pop("session", None)
        if not session:
            return

        query = session.query(object_cls)
        for key, value in kwargs.items():
            query = query.filter(getattr(object_cls, key) == value)

        query.delete()

    def save_import(self, data, file: File, session = None):
        if isinstance(data, data_models.ImportFrom):
            names = ", ".join(data.names)
            import_obj = self.get_object(Import, file=file, module=data.module, session=session)
            if not import_obj:
                import_obj = Import(name=names, file=file, module=data.module)
                session.add(import_obj)
                self.added.add(import_obj)
            else:
                import_obj.name = names
                self.updated.add(import_obj)

        else:
            for import_obj in self.get_object(Import, all_objects=True, file=file, module=None, session=session):
                if import_obj.name == data.names[0]:
                    break
            else:
                new_data = Import(name=data.names[0], file=file)
                session.add(new_data)
                self.added.add(new_data)

    def save_class(self, data, file: File, session = None):
        class_obj = self.get_object(Class, file=file, name=data.name, session=session)
        if not class_obj:
            class_obj = Class(name=data.name, file=file)
            session.add(class_obj)
            self.added.add(class_obj)

        if data.attributes is not None:
            for attribute_data in data.attributes:
                self.save_attribute(attribute_data, file, class_obj, session=session)

        if data.methods is not None:
            for method_data in data.methods:
                self.save_function(method_data, file, class_obj, session=session)

        self.process_delete_objects(Function, data.methods, file=file, class_=class_obj, session=session)

    def save_function(self, data, file: File, class_obj: Class | None = None, session = None):
        function = self.get_object(Function, file=file, class_=class_obj, name=data.name, session=session)
        if not function:
            function = Function(name=data.name, file=file, class_=class_obj)
            session.add(function)
            self.added.add(function)
        else:
            self.updated.add(function)

        function.args = ", ".join(data.args) if data.args else None
        function.decorator_list = ", ".join(data.decorator_list) if data.decorator_list else None
        function.returns = data.returns
        function.is_async = data.is_async

    def save_attribute(self, data, file: File, class_obj: Class | None = None, session = None):
        pass

    def save_file(self, data, module: Module | None = None, session = None):
        file = self.get_object(File, project_id=self.project.id, module=module, name=data.name, session=session)
        if not file:
            file = File(name=data.name, project_id=self.project.id, module=module)
            session.add(file)
            self.added.add(file)

        if data.imports is not None:
            for import_data in data.imports:
                self.save_import(import_data, file, session=session)

        if data.classes is not None:
            for class_data in data.classes:
                self.save_class(class_data, file, session=session)

        if data.functions is not None:
            for function_data in data.functions:
                self.save_function(function_data, file, session=session)

        if data.attributes is not None:
            for attribute_data in data.attributes:
                self.save_attribute(attribute_data, file, session=session)

        self.process_delete_imports(data.imports, file=file, session=session)
        self.process_delete_objects(Class, data.classes, file=file, session=session)
        self.process_delete_objects(Function, data.functions, file=file, class_=None, session=session)

    def save_module(self, data, parent_module: Module | None = None, session = None):
        module = self.get_object(
            Module,
            project_id=self.project.id,
            parent=parent_module,
            name=data.name,
            session=session
        )
        if not module:
            module = Module(name=data.name, project_id=self.project.id, parent=parent_module)
            session.add(module)
            self.added.add(module)

        if data.modules is not None:
            for module_data in data.modules:
                self.save_module(module_data, module, session=session)

        if data.files is not None:
            for file_data in data.files:
                self.save_file(file_data, module, session=session)

        self.process_delete_objects(Module, data.modules, project_id=self.project.id, parent=module, session=session)
        self.process_delete_objects(File, data.files, project_id=self.project.id, module=module, session=session)

    @db_session
    def _save(self, data, session = None):
        for module in data.modules:
            self.save_module(module, session=session)

        for file in data.files:
            self.save_file(file, session=session)

        self.process_delete_objects(Module, data.modules, project_id=self.project.id, parent=None, session=session)
        self.process_delete_objects(File, data.files, project_id=self.project.id, module=None, session=session)

        session.commit()

    def process_delete_imports(self, data, **kwargs):
        if data is None:
            return

        imports = [item for item in data if isinstance(item, data_models.Import)]
        imports_from = [item for item in data if isinstance(item, data_models.ImportFrom)]

        for db_object in self.get_object(Import, all_objects=True, **kwargs):
            if db_object.module is None:
                for object_data in imports:
                    if object_data.names[0] == db_object.name:
                        break
                else:
                    self.delete_objects(Import, id=db_object.id, session=session)
                    self.deleted.add(db_object)

            else:
                for object_data in imports_from:
                    if object_data.module == db_object.module:
                        break
                else:
                    self.delete_objects(Import, id=db_object.id, session=session)
                    self.deleted.add(db_object)

    def process_delete_objects(self, object_cls, data, **kwargs):
        if data is None:
            return

        for db_object in self.get_object(object_cls, all_objects=True, **kwargs):
            for object_data in data:
                if object_data.name == db_object.name:
                    break
            else:
                self.delete_objects(object_cls, id=db_object.id, session=session)
                self.deleted.add(db_object)

    async def save(self, data):
        try:
            self._save(data)
        except Exception as error:
            logging.error(error, exc_info=True)

        self.logger.debug(self.added.result)
        self.logger.debug(self.updated.result)
        self.logger.debug(self.deleted.result)
