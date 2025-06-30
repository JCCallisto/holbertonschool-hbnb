from app.models.base_model import BaseModel
import re
from datetime import datetime

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.password = password
        self.is_admin = is_admin
        self._places = []
        self._reviews = []

    @staticmethod
    def validate_name(name, field_name):
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        if len(name) > 50:
            raise ValueError(f"{field_name} cannot exceed 50 characters")
        return name.strip()

    @staticmethod
    def validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email = email.strip().lower()
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    def add_place(self, place):
        if place not in self._places:
            self._places.append(place)

    def add_review(self, review):
        if review not in self._reviews:
            self._reviews.append(review)

    @property
    def places(self):
        return self._places.copy()

    @property
    def reviews(self):
        return self._reviews.copy()

    def update(self, data):
        if 'first_name' in data:
            self.first_name = self.validate_name(data['first_name'], "First name")
        if 'last_name' in data:
            self.last_name = self.validate_name(data['last_name'], "Last name")
        if 'email' in data:
            self.email = self.validate_email(data['email'])
        if 'password' in data:
            self.password = data['password']
        
        self.updated_at = datetime.now()

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"


class OwnerMixin:
    def __init__(self, owner_id):
        from app.services.facade import facade
        if not owner_id:
            raise ValueError("Owner ID is required")
        
        owner = facade.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        self.owner_id = owner_id
        self._owner = owner
        owner.add_place(self)

    @property
    def owner(self):
        return self._owner
