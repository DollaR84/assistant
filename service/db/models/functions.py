from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, Session

from db.connection import Base


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)

    file_id = Column(
        Integer, ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
    )
    file = relationship(
        "File", uselist=False,
        foreign_keys=file_id,
        back_populates="functions",
    )

    class_id = Column(
        Integer, ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=True, default=None, unique=False,
    )
    class_ = relationship(
        "Class", uselist=False,
        foreign_keys=class_id,
        back_populates="methods",
    )

    args = Column(Text, nullable=True)
    decorator_list = Column(Text, nullable=True)
    returns = Column(Text, nullable=True)
    is_async = Column(Boolean, nullable=False, default=False)

    @property
    def parameters(self):
        return self.args.split(", ") if self.args else []

    @property
    def decorators(self):
        return self.decorator_list.split(", ") if self.decorator_list else []
