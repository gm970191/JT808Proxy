"""
认证API路由
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import logging

from api.models.user import (
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserUpdate,
    UserResponse
)
from api.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["认证管理"])

# HTTP Bearer认证
security = HTTPBearer()

# 依赖注入
def get_auth_service():
    """获取认证服务实例"""
    return AuthService()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """获取当前用户依赖"""
    token = credentials.credentials
    user = auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """用户登录"""
    try:
        # 验证用户
        user = auth_service.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        
        # 创建访问令牌
        access_token = auth_service.create_access_token(
            data={"sub": user['username'], "user_id": user['id'], "role": user['role']}
        )
        
        logger.info(f"用户登录成功: {login_data.username}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,
            user=UserResponse(**user)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户登录失败: {e}")
        raise HTTPException(status_code=500, detail="登录失败")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户信息"""
    return UserResponse(**current_user)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """创建用户（需要管理员权限）"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 创建用户
        user = auth_service.create_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            role=user_data.role
        )
        
        logger.info(f"创建用户成功: {user_data.username}")
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        raise HTTPException(status_code=500, detail="创建用户失败")

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="页大小"),
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """获取用户列表（需要管理员权限）"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 获取用户列表
        users = auth_service.get_users(offset=offset, limit=size)
        
        return [UserResponse(**user) for user in users]
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取用户列表失败")

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """更新用户信息（需要管理员权限或本人）"""
    try:
        # 检查权限
        if current_user['role'] != 'admin' and current_user['id'] != user_id:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 更新用户信息
        user = auth_service.update_user(
            user_id=user_id,
            password=user_update.password,
            email=user_update.email,
            role=user_update.role
        )
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        logger.info(f"更新用户信息成功: {user_id}")
        return UserResponse(**user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        raise HTTPException(status_code=500, detail="更新用户信息失败")

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """删除用户（需要管理员权限）"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 不能删除自己
        if current_user['id'] == user_id:
            raise HTTPException(status_code=400, detail="不能删除自己")
        
        # 删除用户
        success = auth_service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        logger.info(f"删除用户成功: {user_id}")
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        raise HTTPException(status_code=500, detail="删除用户失败") 