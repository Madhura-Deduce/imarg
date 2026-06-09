from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True)

    action_type = Column(String, index=True)
    # e.g. bbox_draw, area_calculate, poi_search, routing

    area_sqkm = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)