from .base import BaseEntity

class Amenity(BaseEntity):
    def __init__(self, name):
        super().__init__(name=name)

    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Amenity name cannot be empty")
