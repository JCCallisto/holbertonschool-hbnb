from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        d = super().to_dict()
        del d['password']
        return d
