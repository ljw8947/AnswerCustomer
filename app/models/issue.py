import uuid
from datetime import datetime

class Issue:
    def __init__(self,
                 issue_id: str = None,
                 create_time: str = None,
                 carline: str = None,
                 power: str = None,
                 specific_function: str = None,
                 function_domain: str = None,
                 general_domain: str = None,
                 issue_type: str = None,
                 description: str = None,
                 description_en: str = None,
                 brief_issue: str = None,
                 brief_issue_en: str = None,
                 global_id: int = None,
                 user_issue_id: int = None,
                 created_by_user_id: str = None,
                 status: str = 'New',  # New field: 'New', 'Assigned', 'In Progress', 'Resolved', 'Closed'
                 assigned_to_user_id: str = None, # New field: ID of the engineer assigned
                 extra_info: str = None, # New field: Additional info for status updates
                 notified: int = 0,  # New field: Email notification status (0=not notified, 1=notified)
                 batch: str = None  # 新增字段: 批次信息
                 ):
        self.issue_id = issue_id if issue_id else str(uuid.uuid4())
        self.create_time = create_time if create_time else datetime.now().strftime("%Y-%m-%d")
        self.carline = carline
        self.power = power
        self.specific_function = specific_function
        self.function_domain = function_domain
        self.general_domain = general_domain
        self.issue_type = issue_type
        self.description = description
        self.description_en = description_en
        self.brief_issue = brief_issue
        self.brief_issue_en = brief_issue_en
        self.global_id = global_id
        self.user_issue_id = user_issue_id
        self.created_by_user_id = created_by_user_id
        self.status = status
        self.assigned_to_user_id = assigned_to_user_id
        self.extra_info = extra_info
        self.notified = notified
        self.batch = batch

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an Issue instance from a dictionary."""
        # Helper function to safely convert to int
        def safe_int(value):
            try:
                return int(value) if value is not None and value != '' else None
            except (ValueError, TypeError):
                return None

        return cls(
            issue_id=data.get('issue_id'),
            create_time=data.get('create_time'),
            carline=data.get('carline'),
            power=data.get('power'),
            specific_function=data.get('specific_function'),
            function_domain=data.get('function_domain'),
            general_domain=data.get('general_domain'),
            issue_type=data.get('issue_type'),
            description=data.get('description'),
            description_en=data.get('description_en'),
            brief_issue=data.get('brief_issue'),
            brief_issue_en=data.get('brief_issue_en'),
            # Safely convert global_id and user_issue_id to int or None
            global_id=safe_int(data.get('global_id')),
            user_issue_id=safe_int(data.get('user_issue_id')),
            created_by_user_id=data.get('created_by_user_id'),
            status=data.get('status', 'New'),
            assigned_to_user_id=data.get('assigned_to_user_id'),
            extra_info=data.get('extra_info') or None,  # 确保None值被正确处理
            notified=safe_int(data.get('notified')) or 0,  # 使用safe_int确保正确转换
            batch=data.get('batch')
        )

    def to_dict(self):
        """Converts the Issue instance to a dictionary."""
        return {
            'issue_id': self.issue_id,
            'create_time': self.create_time,
            'carline': self.carline,
            'power': self.power,
            'specific_function': self.specific_function,
            'function_domain': self.function_domain,
            'general_domain': self.general_domain,
            'issue_type': self.issue_type,
            'description': self.description,
            'description_en': self.description_en,
            'brief_issue': self.brief_issue,
            'brief_issue_en': self.brief_issue_en,
            'global_id': self.global_id,
            'user_issue_id': self.user_issue_id,
            'created_by_user_id': self.created_by_user_id,
            'status': self.status,
            'assigned_to_user_id': self.assigned_to_user_id,
            'extra_info': self.extra_info,
            'notified': self.notified,
            'batch': self.batch
        }

    def __repr__(self):
        return f"""Issue(issue_id='{self.issue_id}', brief_issue='{self.brief_issue}', global_id={self.global_id}, status='{self.status}')""" 