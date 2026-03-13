class WaterTest(Base):
    __tablename__ = "water_tests"

    id = Column(Integer, primary_key=True)

    tank_id = Column(Integer, ForeignKey("tanks.id"))

    ammonia = Column(String)
    nitrite = Column(String)
    nitrate = Column(String)
    ph = Column(String)
    temperature = Column(String)
