from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from db.connection import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)

    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    project = relationship(
        "Project", uselist=False,
        foreign_keys=project_id,
        back_populates="projects_modules",
    )

    parent_id = Column(
        Integer, ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=True, default=None, unique=False,
    )
    parent = relationship(
        "Module", uselist=False,
        primaryjoin=parent_id == id,
        foreign_keys=parent_id, remote_side=id,
        back_populates="childs_modules",
    )

    childs_modules = relationship(
        "Module", back_populates="parent",
    )

    modules_files = relationship(
        "File", back_populates="module",
    )
