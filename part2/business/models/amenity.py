from .base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "name": self.name,
        })
        return d
