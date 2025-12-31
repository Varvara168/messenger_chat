from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserStatusBase(BaseModel):
    user_id: int
    is_online: bool
    last_seen: datetime
    last_activity: datetime

class UserStatusOut(UserStatusBase):
    id: int
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserStatusUpdate(BaseModel):
    is_online: Optional[bool] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None

class UserLastSeen(BaseModel):
    user_id: int
    first_name: str
    short_name: str
    is_online: bool
    last_seen: datetime
    last_activity: datetime
    formatted_last_seen: str

class BatchStatusRequest(BaseModel):
    user_ids: list[int]

class BatchStatusResponse(BaseModel):
    statuses: dict[int, dict]