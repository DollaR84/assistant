from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from db.connection import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)

    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    project = relationship(
        "Project", uselist=False,
        foreign_keys=project_id,
        back_populates="projects_files",
    )

    module_id = Column(
        Integer, ForeignKey("modules.id", ondelete="SET NULL"),
        nullable=True, default=None, unique=False,
    )
    module = relationship(
        "Module", uselist=False,
        foreign_keys=module_id,
        back_populates="modules_files",
    )

    imports = relationship(
        "Import", back_populates="file",
    )

    classes = relationship(
        "Class", back_populates="file",
    )

    functions = relationship(
        "Function", back_populates="file",
    )
