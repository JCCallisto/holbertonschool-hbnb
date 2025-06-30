from app.models.base_model import BaseModel
from datetime import datetime

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return name.strip()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        if 'name' in data:
            self.name = self.validate_name(data['name'])
        
        self.updated_at = datetime.now()
