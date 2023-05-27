import logging
import sys

from flask import Flask, request, send_from_directory
from sqlalchemy import create_engine, text

from db.db_creator import create_db
from config.config_reader import get_config
from logs.logger import setup_logger
from monitor.monitor import CPUMonitor


if __name__ == "__main__":
    logger = setup_logger()

    logger.debug("Starting get_config().")
    config = get_config()
    if "Error" in config:
        logger.debug("The configuration has been loaded successfully.")
        sys.exit()

    engine = create_engine(f'{config["db_config"]["db_dialect"]}://{config["db_config"]["db_path"]}')
    create_db(engine)

    logger.debug("Starting CPU load recording.")
    CPUMonitor(engine).start_record()
    logger.debug("CPU load recording started successfully.")