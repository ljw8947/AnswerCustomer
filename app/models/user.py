import uuid
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,
                 username: str = None,
                 email: str = None,
                 password_hash: str = None,
                 role: str = 'engineer',  # 默认为工程师
                 status: str = 'active',
                 user_id: str = None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status
        self.user_id = user_id if user_id else str(uuid.uuid4())

    def get_id(self):
        """Flask-Login 需要的方法"""
        return self.username

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建用户实例"""
        return cls(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=data.get('role', 'engineer'),
            status=data.get('status', 'active'),
            user_id=data.get('user_id')
        )

    def to_dict(self):
        """转换为字典"""
        return {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'status': self.status,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f"User(username='{self.username}', role='{self.role}', status='{self.status}')" 