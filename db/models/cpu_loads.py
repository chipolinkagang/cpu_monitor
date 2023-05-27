import uuid
import datetime

from sqlalchemy import Column, Integer, String, select, update, text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# from utils.file_funcs import FileSystem

# filesys = FileSystem()
Base = declarative_base()


class CpuLoads(Base):
    __tablename__ = 'cpu_loads'
    id = Column(Integer, primary_key=True)
    load = Column(Float)
    load_date = Column(DateTime(timezone=True))

    def add_load(self, engine):
        with Session(engine) as session:
            try:
                session.add(CpuLoads(name=self.id,
                                     extension=self.load,
                                     size=self.load_date
                                     ))
                session.commit()
                return True
            except Exception as e:
                return False

    # def get_last_hour_loads(self, engine):

