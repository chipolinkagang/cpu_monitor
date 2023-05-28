import uuid
import datetime

from sqlalchemy import Column, Integer, String, select, update, text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# from utils.file_funcs import FileSystem

# filesys = FileSystem()
Base = declarative_base()


class CPULoads(Base):
    __tablename__ = 'cpu_loads'
    id = Column(Integer, primary_key=True)
    load = Column(Float)
    load_date = Column(DateTime(timezone=True))

    def add_load(self, engine) -> bool:
        with Session(engine) as session:
            try:
                session.add(CPULoads(load=self.load,
                                     load_date=self.load_date
                                     ))
                session.commit()
                return True
            except Exception as e:
                return False

    def get_last_hour_loads(self, engine, dtime=datetime.timedelta(hours=1)) -> list[dict]:
        time = datetime.datetime.now()
        time -= dtime
        points = []

        stmt = select(CPULoads).filter(CPULoads.load_date >= time).order_by(CPULoads.load_date)
        with Session(engine) as session:
            for row in session.scalars(stmt):
                points.append({"time": row.load_date, "value": row.load})
        return points