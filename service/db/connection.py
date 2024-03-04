from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base

from config import Config


cfg = Config()


engine = create_engine(
    cfg.db_url, encoding="utf8",
    echo=cfg.DEBUG_SQLALCHEMY,
    pool_pre_ping=True,
)


session_maker = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)
