import json
import logging
import random
import sys
import time
from datetime import datetime

from flask import Flask, request, send_from_directory, render_template, Response, stream_with_context
from sqlalchemy import create_engine, text

from db.db_creator import create_db
from config.config_reader import get_config
from db.models.cpu_loads import CPULoads
from logs.logger import setup_logger
from monitor.monitor import CPUMonitor
from utils.utils import fill_space, get_average_values

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        cpu_monitor = CPULoads()
        data_list = cpu_monitor.get_last_hour_loads(engine)
        data_list = fill_space(data_list, 720, 5)

        json_data = json.dumps(data_list)

        yield f"data:{json_data}\n\n"
        time.sleep(5)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.route('/avg-chart-data')
def avg_chart_data():
    def generate_random_data():
        cpu_monitor = CPULoads()
        data_list = cpu_monitor.get_last_hour_loads(engine)
        data_list = fill_space(data_list, 720, 5)
        avg_data = get_average_values(data_list, 720, 12)

        json_avg_data = json.dumps(avg_data)

        yield f"data:{json_avg_data}\n\n"
        time.sleep(5)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


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
    monitor = CPUMonitor(engine)
    monitor.start_record()
    logger.debug("CPU load recording started successfully.")

    app.run(host='0.0.0.0', port=5000)