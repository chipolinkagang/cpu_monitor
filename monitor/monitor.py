import datetime
import threading
from psutil import cpu_percent

from db.models.cpu_loads import CPULoads
from logs.logger import setup_logger


class CPUMonitor:

    def __init__(self, inp_engine):
        self.engine = inp_engine
        self.logger = setup_logger()

    def record_load(self):
        while True:
            temp_load = cpu_percent(interval=5)
            print(temp_load)
            self.logger.info(f"{temp_load}%")
            CPULoads(load=temp_load, load_date=datetime.datetime.now()).add_load(self.engine)

    def start_record(self):
        self.logger.debug("Start recording.")
        monitor_thread = threading.Thread(target=self.record_load(), daemon=True)
        monitor_thread.start()