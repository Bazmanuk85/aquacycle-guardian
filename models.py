from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    tanks = relationship("Tank", back_populates="owner")


class Tank(Base):
    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    volume = Column(Integer)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tanks")


class WaterTest(Base):
    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    ammonia = Column(String)
    nitrite = Column(String)
    nitrate = Column(String)
    ph = Column(String)
    temperature = Column(String)
