import ast
import logging
import os

from config import Config

from .data import Attribute, Class, File, Function, Import, ImportFrom, Module


class DataLoader:

    def __init__(self, project_name: str):
        self.cfg = Config()
        self.project_name = project_name

        self.logger = logging.getLogger("debugger")

    def get_data(self):
        project_path = self.cfg.projects[self.project_name]
        work_subfolder = self.cfg.work_subfolders.get(self.project_name)

        root = os.path.join(project_path, work_subfolder) if work_subfolder else project_path
        return self.search(root)

    def check_excludes(self, path: str):
        exclude_list = ("__pycache__", "pytest_cache",)
        for exclude in exclude_list:
            if exclude in path:
                return False
        return True

    def search(self, path: str):
        module_name = os.path.split(path)[1]
        module = Module(name=module_name)
        names = os.listdir(path)

        folders = [
            os.path.join(path, name)
            for name in names
            if os.path.isdir(os.path.join(path, name)) and self.check_excludes(name)
        ]

        files = [
            os.path.join(path, name)
            for name in names
            if os.path.isfile(os.path.join(path, name)) and name.endswith(".py")
        ]

        module.files = [self.process_file(file_path) for file_path in files]
        module.modules = [self.search(path) for path in folders]

        return module

    def process_file(self, file_path: str):
        file_name = os.path.split(file_path)[1]
        file_name = os.path.splitext(file_name)[0]

        data = self.process_data(file_path)
        return File(name=file_name, **data)

    def process_data(self, file_path: str):
        data = {}
        with open(file_path, "r") as file_:
            try:
                parsed_ast = ast.parse(file_.read())
            except Exception as error:
                logger = logging.getLogger()
                logger.error(file_path)
                logger.error(error, exc_info=True)
                return data

            imports = [
                node
                for node in ast.walk(parsed_ast)
                if isinstance(node, (ast.Import, ast.ImportFrom))
            ]
            data["imports"] = self.process_imports(imports)

            functions = [
                node
                for node in ast.walk(parsed_ast)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            data["functions"] = self.process_functions(functions)

            attributes = []
            data["attributes"] = self.process_attributes(attributes)

            classes = [
                (node, [
                ], [
                    n for n in ast.walk(node)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ],)
                for node in ast.walk(parsed_ast)
                if isinstance(node, ast.ClassDef)
            ]
            data["classes"] = self.process_classes(classes)

        return data

    def process_imports(self, imports):
        results = []
        for item in imports:
            if isinstance(item, ast.ImportFrom):
                result = ImportFrom(module=item.module)
            else:
                result = Import()
            result.names = [alias.name for alias in item.names]
        return results

    def get_decorator_value(self, decorator):
        value = ""
        if isinstance(decorator, ast.Name):
            value = decorator.id
        elif isinstance(decorator, ast.Attribute):
            value = decorator.attr
        return value

    def process_functions(self, functions):
        return [
            Function(
                name=item.name,
                args=[arg.arg for arg in item.args.args],
                decorator_list=[self.get_decorator_value(decorator) for decorator in item.decorator_list],
                returns=None,
                is_async=isinstance(item, ast.AsyncFunctionDef),
            )
            for item in functions
        ]

    def process_attributes(self, attributes):
        return []

    def process_classes(self, classes):
        return [
            Class(
                name=item.name,
                attributes=self.process_attributes(attributes),
                methods=self.process_functions(methods),
            )
            for item, attributes, methods in classes
        ]
