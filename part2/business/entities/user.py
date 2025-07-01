import re
from .base import BaseEntity

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

class User(BaseEntity):
    def __init__(self, email, password, first_name=None, last_name=None):
        super().__init__(email=email, first_name=first_name, last_name=last_name)
        self.password = password

    def validate(self):
        if not self.email or not EMAIL_REGEX.match(self.email):
            raise ValueError("Invalid email format")
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.password or len(self.password) < 4:
            raise ValueError("Password too short")
