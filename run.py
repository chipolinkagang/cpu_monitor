from flask import Flask, request, send_from_directory
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

from db.models.cpu_loads import CpuLoads
from config.config_reader import get_config

config = get_config()
engine = create_engine(f'{config["db_config"]["db_dialect"]}:///{config["db_config"]["db_path"]}')
if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as con:
        con.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
Base = declarative_base()
Base.metadata.create_all(engine, tables=[CpuLoads.__table__])

