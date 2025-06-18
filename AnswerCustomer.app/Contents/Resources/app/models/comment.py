import uuid
from datetime import datetime

class Comment:
    def __init__(self, comment_id=None, issue_id=None, user_id=None, username=None, content=None, created_at=None):
        self.comment_id = comment_id or str(uuid.uuid4())
        self.issue_id = issue_id
        self.user_id = user_id
        self.username = username
        self.content = content
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'issue_id': self.issue_id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            comment_id=data.get('comment_id'),
            issue_id=data.get('issue_id'),
            user_id=data.get('user_id'),
            username=data.get('username'),
            content=data.get('content'),
            created_at=data.get('created_at')
        ) 