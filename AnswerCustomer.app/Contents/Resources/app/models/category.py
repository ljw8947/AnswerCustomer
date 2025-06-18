import uuid
from datetime import datetime

class Category:
    def __init__(self, category_id=None, specific_function=None, function_domain=None, general_domain=None, email_list=None, created_at=None, updated_at=None):
        self.category_id = category_id or str(uuid.uuid4())
        self.specific_function = specific_function
        self.function_domain = function_domain
        self.general_domain = general_domain
        self.email_list = email_list or ""
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = updated_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'specific_function': self.specific_function,
            'function_domain': self.function_domain,
            'general_domain': self.general_domain,
            'email_list': self.email_list,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            category_id=data.get('category_id'),
            specific_function=data.get('specific_function'),
            function_domain=data.get('function_domain'),
            general_domain=data.get('general_domain'),
            email_list=data.get('email_list', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def get_email_list(self):
        """获取邮箱列表，返回列表格式"""
        if not self.email_list:
            return []
        return [email.strip() for email in self.email_list.split(',') if email.strip()]
    
    def set_email_list(self, emails):
        """设置邮箱列表，接受列表格式"""
        self.email_list = ','.join(emails) if emails else ""
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 