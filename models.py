from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    password = Column(String)

    email_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Tank(Base):

    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    tank_type = Column(String)

    size_litres = Column(Float)


class Fish(Base):

    __tablename__ = "fish"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer)

    species = Column(String)

    quantity = Column(Integer)


class WaterTest(Base):

    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer)

    ammonia = Column(Float, nullable=True)

    nitrite = Column(Float, nullable=True)

    nitrate = Column(Float, nullable=True)

    ph = Column(Float, nullable=True)

    temperature = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)


class WaterChange(Base):

    __tablename__ = "water_changes"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer)

    percent = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)
