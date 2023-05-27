from flask import Flask, request, send_from_directory
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

from db.models.cpu_loads import CPULoads
from config.config_reader import get_config
from monitor.monitor import CPUMonitor

config = get_config()
engine = create_engine(f'{config["db_config"]["db_dialect"]}://{config["db_config"]["db_path"]}')
if not database_exists(engine.url):
    create_database(engine.url)
Base = declarative_base()
Base.metadata.create_all(engine, tables=[CPULoads.__table__])

if __name__ == "__main__":
    CPUMonitor(engine).start_record()