from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    solidity_code = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=True)  # Changed from JSON to Text
    risk_score = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())