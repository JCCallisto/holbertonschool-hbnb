from .base import BaseModel

class User(BaseModel):
    def __init__(self, email, first_name, last_name, password, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password  # Should not be exposed in API responses

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        })
        return d
