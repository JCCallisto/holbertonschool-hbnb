import uuid
from datetime import datetime

class BaseEntity:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        self.created_at = now
        self.updated_at = now
        for k, v in kwargs.items():
            setattr(self, k, v)
    def save(self):
        self.updated_at = datetime.utcnow().isoformat()
