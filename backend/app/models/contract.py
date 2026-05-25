from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database.connection import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    solidity_code = Column(Text, nullable=False)
    analysis_result = Column(JSON, nullable=True)
    risk_score = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())