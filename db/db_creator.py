from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

from db.models.cpu_loads import CPULoads
from logs.logger import setup_logger


def create_db(engine):
    logger = setup_logger()
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.debug("Database was created.")
    Base = declarative_base()
    Base.metadata.create_all(engine, tables=[CPULoads.__table__])