from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session

from db.connection import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(256), nullable=False, unique=True)
    path = Column(String(256), nullable=False)
    work_subfolder = Column(String(256), nullable=True)

    projects_modules = relationship(
        "Module", back_populates="project",
    )

    projects_files = relationship(
        "File", back_populates="project",
    )

    def __str__(self):
        return " ".join(["Project", self.name, "#{}".format(self.id)])
