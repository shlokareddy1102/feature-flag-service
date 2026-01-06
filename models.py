from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    enabled = Column(Boolean, default=False)
    rollout_percentage = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FeatureLog(Base):
    __tablename__ = "feature_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    feature_name = Column(String, index=True)

    result = Column(Boolean)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


