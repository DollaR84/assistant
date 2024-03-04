from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from db.connection import Base


class Import(Base):
    __tablename__ = "imports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    module_ = Column(String(256), nullable=True, default=None)

    file_id = Column(
        Integer, ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
    )
    file = relationship(
        "File", uselist=False,
        foreign_keys=file_id,
        back_populates="imports",
    )
