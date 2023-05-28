import datetime
import threading
import time

from psutil import cpu_percent

from db.models.cpu_loads import CPULoads
from logs.logger import setup_logger


class CPUMonitor:

    def __init__(self, inp_engine):
        self.engine = inp_engine
        self.logger = setup_logger()

    def record_load(self):
        temp_load = cpu_percent()
        print(temp_load, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.logger.info(f"{temp_load}%")
        CPULoads(load=temp_load, load_date=datetime.datetime.now()).add_load(self.engine)

    def start_load(self):
        while True:
            self.record_load()
            time.sleep(5)

    def start_record(self):
        self.logger.debug("Start recording.")
        monitor_thread = threading.Thread(target=self.start_load, daemon=True)
        monitor_thread.start()