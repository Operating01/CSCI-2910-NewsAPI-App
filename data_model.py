from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Domains(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True)
    domain = Column(String)
    include = Column(String)
    
    def __repr__(self):
        return f"{self.domain}: is currently set to {self.include}."