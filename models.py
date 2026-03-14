from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class Tank(Base):
    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tank_type = Column(String)

    tests = relationship("WaterTest", back_populates="tank")
    water_changes = relationship("WaterChange", back_populates="tank")


class WaterTest(Base):
    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True, index=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    ammonia = Column(Float)
    nitrite = Column(Float)
    nitrate = Column(Float)

    ph = Column(Float)
    temperature = Column(Float)

    tank = relationship("Tank", back_populates="tests")


class WaterChange(Base):
    __tablename__ = "water_changes"

    id = Column(Integer, primary_key=True, index=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    percent = Column(Float)

    tank = relationship("Tank", back_populates="water_changes")
