from db.models import Class, File, Function, Import, Module


class BaseResultCount:

    def __init__(self):
        self.imports: int = 0
        self.functions: int = 0
        self.classes: int = 0
        self.files: int = 0
        self.modules: int = 0

    def add(self, object_):
        if isinstance(object_, Import):
            self.imports += 1
        elif isinstance(object_, Function):
            self.functions += 1
        elif isinstance(object_, Class):
            self.classes += 1
        elif isinstance(object_, File):
            self.files += 1
        elif isinstance(object_, Module):
            self.modules += 1

    @property
    def result(self):
        return ", ".join([
            f"modules: {self.modules}",
            f"files: {self.files}",
            f"classes: {self.classes}",
            f"functions: {self.functions}",
            f"imports: {self.imports}",
        ])


class ResultCountAdd(BaseResultCount):

    @property
    def result(self):
        return "\n".join(["Added:", super().result])


class ResultCountUpdate(BaseResultCount):

    @property
    def result(self):
        return "\n".join(["Updated:", super().result])


class ResultCountDelete(BaseResultCount):

    @property
    def result(self):
        return "\n".join(["Deleted:", super().result])
