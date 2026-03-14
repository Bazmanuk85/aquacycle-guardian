from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Tank(Base):
    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tank_type = Column(String)

    tests = relationship("WaterTest", back_populates="tank")
    changes = relationship("WaterChange", back_populates="tank")


class WaterTest(Base):
    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True, index=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    ammonia = Column(Float, nullable=True)
    nitrite = Column(Float, nullable=True)
    nitrate = Column(Float, nullable=True)
    ph = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    tank = relationship("Tank", back_populates="tests")


class WaterChange(Base):
    __tablename__ = "water_changes"

    id = Column(Integer, primary_key=True, index=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    percent = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

    tank = relationship("Tank", back_populates="changes")
