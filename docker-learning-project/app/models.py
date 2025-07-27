from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Kullanıcı email adresi")
    name: str = Field(..., min_length=2, max_length=100, description="Kullanıcı adı")
    password: str = Field(..., min_length=6, description="Şifre")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Kullanıcı email adresi")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Kullanıcı adı")
    is_active: Optional[bool] = Field(None, description="Kullanıcı aktif durumu")

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    database: bool
    cache: bool
    version: str

class ServiceInfo(BaseModel):
    name: str
    version: str
    description: str
    environment: str
    database_url: str
    redis_url: str

class MetricsResponse(BaseModel):
    timestamp: datetime
    user_count: int
    cache_status: bool
    uptime: str 