from dataclasses import dataclass


@dataclass
class Function:
    name: str
    args: list[str] | None = None
    decorator_list: list[str] | None = None
    returns: str | None = None
    is_async: bool = False


@dataclass
class Attribute:
    name: str


@dataclass
class Class:
    name: str
    attributes: list[Attribute] | None = None
    methods: list[Function] | None = None


@dataclass
class Import:
    names: list[str] | None = None


@dataclass
class ImportFrom:
    module: str
    names: list[str] | None = None


@dataclass
class File:
    name: str
    imports: list[Import | ImportFrom] | None = None
    classes: list[Class] | None = None
    functions: list[Function] | None = None
    attributes: list[Attribute] | None = None


@dataclass
class Module:
    name: str
    modules: list["Module"] | None = None
    files: list[File] | None = None
