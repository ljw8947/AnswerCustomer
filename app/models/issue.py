import uuid
from datetime import datetime

class Issue:
    def __init__(self,
                 issue_id: str = None,
                 create: str = None,
                 carline: str = None,
                 # power: str = None, # Removed
                 specific_function: str = None,
                 # function: str = None, # Removed
                 general: str = None,
                 issue_type: str = None,
                 description: str = None,
                 brief_issue: str = None,
                 global_id: int = None,
                 user_issue_id: int = None,
                 created_by_user_id: str = None,
                 status: str = 'New',  # New field: 'New', 'Assigned', 'In Progress', 'Resolved', 'Closed'
                 assigned_to_user_id: str = None, # New field: ID of the engineer assigned
                 extra_info: str = None # New field: Additional info for status updates
                 ):
        self.issue_id = issue_id if issue_id else str(uuid.uuid4())
        self.create = create if create else datetime.now().strftime("%Y-%m-%d")
        self.carline = carline
        # self.power = power # Removed
        self.specific_function = specific_function
        # self.function = function # Removed
        self.general = general
        self.issue_type = issue_type
        self.description = description
        self.brief_issue = brief_issue
        self.global_id = global_id
        self.user_issue_id = user_issue_id
        self.created_by_user_id = created_by_user_id
        self.status = status
        self.assigned_to_user_id = assigned_to_user_id
        self.extra_info = extra_info

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
            create=data.get('create'),
            carline=data.get('carline'),
            # power=data.get('power'), # Removed
            specific_function=data.get('specific_function'),
            # function=data.get('function'), # Removed
            general=data.get('general'),
            issue_type=data.get('issue_type'),
            description=data.get('description'),
            brief_issue=data.get('brief_issue'),
            # Safely convert global_id and user_issue_id to int or None
            global_id=safe_int(data.get('global_id')),
            user_issue_id=safe_int(data.get('user_issue_id')),
            created_by_user_id=data.get('created_by_user_id'),
            status=data.get('status', 'New'),
            assigned_to_user_id=data.get('assigned_to_user_id'),
            extra_info=data.get('extra_info')
        )

    def to_dict(self):
        """Converts the Issue instance to a dictionary."""
        return {
            'issue_id': self.issue_id,
            'create': self.create,
            'carline': self.carline,
            # 'power': self.power, # Removed
            'specific_function': self.specific_function,
            # 'function': self.function, # Removed
            'general': self.general,
            'issue_type': self.issue_type,
            'description': self.description,
            'brief_issue': self.brief_issue,
            'global_id': self.global_id,
            'user_issue_id': self.user_issue_id,
            'created_by_user_id': self.created_by_user_id,
            'status': self.status,
            'assigned_to_user_id': self.assigned_to_user_id,
            'extra_info': self.extra_info
        }

    def __repr__(self):
        return f"""Issue(issue_id='{self.issue_id}', brief_issue='{self.brief_issue}', global_id={self.global_id}, status='{self.status}')""" 