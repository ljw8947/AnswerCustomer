import uuid
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,
                 user_id: str = None,
                 username: str = None,
                 email: str = None,
                 password_hash: str = None,
                 role: str = 'user',  # 'admin', 'engineer', or 'user'
                 status: str = 'active',  # 'active', 'inactive', 'suspended', or 'pending'
                 avatar_url: str = None,
                 employee_id: str = None  # 工程师工号
                 ):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status
        self.avatar_url = avatar_url
        self.employee_id = employee_id  # 工程师工号

    def get_id(self):
        """Flask-Login 需要的方法，返回用户的唯一标识符"""
        return self.username  # 使用 username 作为唯一标识符

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建用户实例"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=data.get('role', 'user'),
            status=data.get('status', 'active'),
            avatar_url=data.get('avatar_url'),
            employee_id=data.get('employee_id')  # 从字典中获取工号
        )

    def to_dict(self):
        """将用户实例转换为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'status': self.status,
            'avatar_url': self.avatar_url,
            'employee_id': self.employee_id  # 将工号添加到字典中
        }

    def __repr__(self):
        return f"User(username='{self.username}', role='{self.role}', status='{self.status}')" 