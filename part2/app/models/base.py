import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    def to_dict(self):
        d = self.__dict__.copy()
        d['created_at'] = self.created_at.isoformat()
        d['updated_at'] = self.updated_at.isoformat()
        return d
