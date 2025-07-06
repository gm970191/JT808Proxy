"""
认证服务
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jt808proxy.storage.database import DatabaseManager

logger = logging.getLogger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "jt808proxy-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    """认证服务类"""
    
    def __init__(self):
        """初始化认证服务"""
        self.db_manager = DatabaseManager()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希"""
        return pwd_context.hash(password)
    
    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """验证用户"""
        try:
            # 从数据库获取用户
            user = self.db_manager.get_user_by_username(username)
            if not user:
                return None
            
            # 验证密码
            if not self.verify_password(password, user.get('password_hash', '')):
                return None
            
            # 更新最后登录时间
            self.db_manager.update_user_last_login(user['id'])
            
            return user
        except Exception as e:
            logger.error(f"用户认证失败: {e}")
            return None
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return payload
        except jwt.PyJWTError:
            return None
    
    def get_current_user(self, token: str) -> Optional[dict]:
        """获取当前用户"""
        try:
            payload = self.verify_token(token)
            if payload is None:
                return None
            
            username: str = payload.get("sub")
            if username is None:
                return None
            
            user = self.db_manager.get_user_by_username(username)
            return user
        except Exception as e:
            logger.error(f"获取当前用户失败: {e}")
            return None
    
    def create_user(self, username: str, password: str, email: str = None, role: str = "user") -> Optional[dict]:
        """创建用户"""
        try:
            # 检查用户名是否已存在
            existing_user = self.db_manager.get_user_by_username(username)
            if existing_user:
                raise ValueError(f"用户名 {username} 已存在")
            
            # 创建用户
            user_id = self.db_manager.create_user(
                username=username,
                password_hash=self.get_password_hash(password),
                email=email,
                role=role
            )
            
            # 获取创建的用户信息
            user = self.db_manager.get_user_by_username(username)
            return user
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise
    
    def update_user(self, user_id: int, **kwargs) -> Optional[dict]:
        """更新用户信息"""
        try:
            update_data = {}
            
            if 'password' in kwargs:
                update_data['password_hash'] = self.get_password_hash(kwargs['password'])
            
            if 'email' in kwargs:
                update_data['email'] = kwargs['email']
            
            if 'role' in kwargs:
                update_data['role'] = kwargs['role']
            
            if not update_data:
                return None
            
            # 更新用户信息
            self.db_manager.update_user(user_id, update_data)
            
            # 获取更新后的用户信息
            user = self.db_manager.get_user_by_id(user_id)
            return user
        except Exception as e:
            logger.error(f"更新用户信息失败: {e}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        try:
            return self.db_manager.delete_user(user_id)
        except Exception as e:
            logger.error(f"删除用户失败: {e}")
            raise
    
    def get_users(self, offset: int = 0, limit: int = 20) -> list:
        """获取用户列表"""
        try:
            return self.db_manager.get_users(offset=offset, limit=limit)
        except Exception as e:
            logger.error(f"获取用户列表失败: {e}")
            raise 