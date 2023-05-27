import datetime
import threading

from psutil import cpu_percent
from db.models.cpu_loads import CPULoads


class CPUMonitor:
    engine = 0

    def __init__(self, inp_engine):
        self.engine = inp_engine

    def record_load(self):
        while True:
            temp_load = cpu_percent(interval=5)
            print(temp_load)
            CPULoads(load=temp_load, load_date=datetime.datetime.now()).add_load(self.engine)

    def start_record(self):
        monitor_thread = threading.Thread(target=self.record_load(), daemon=True)
        monitor_thread.start()