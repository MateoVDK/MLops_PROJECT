from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    player_sum = Column(Integer, nullable=False)
    dealer_card = Column(Integer, nullable=False)
    usable_ace = Column(Boolean, nullable=False)
    action = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=True)
    premium = Column(Boolean, nullable=False, default=False)
