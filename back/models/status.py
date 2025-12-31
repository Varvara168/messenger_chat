from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime, timezone
from db import Base

class UserStatus(Base):
    __tablename__ = "user_status"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True, index=True)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    device_info = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<UserStatus(user_id={self.user_id}, online={self.is_online})>"