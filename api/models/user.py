"""
用户数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """用户基础信息"""
    username: str = Field(..., description="用户名")
    email: Optional[str] = Field(None, description="邮箱")
    role: str = Field("user", description="用户角色")

class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., description="密码")

class UserUpdate(BaseModel):
    """更新用户信息"""
    email: Optional[str] = Field(None, description="邮箱")
    role: Optional[str] = Field(None, description="用户角色")
    password: Optional[str] = Field(None, description="密码")

class UserResponse(UserBase):
    """用户信息响应"""
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(3600, description="过期时间(秒)")
    user: UserResponse = Field(..., description="用户信息")

class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None 