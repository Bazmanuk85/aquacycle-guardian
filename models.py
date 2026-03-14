from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Tank(Base):

    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tank_type = Column(String)

    tests = relationship("WaterTest", back_populates="tank")
    water_changes = relationship("WaterChange", back_populates="tank")


class WaterTest(Base):

    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    ammonia = Column(Float, nullable=True)
    nitrite = Column(Float, nullable=True)
    nitrate = Column(Float, nullable=True)

    ph = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)

    tank = relationship("Tank", back_populates="tests")


class WaterChange(Base):

    __tablename__ = "water_changes"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    percent = Column(Float)

    tank = relationship("Tank", back_populates="water_changes")
