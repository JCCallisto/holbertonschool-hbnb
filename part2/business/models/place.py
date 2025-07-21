from .base import BaseModel

class Place(BaseModel):
    def __init__(self, name, owner_id, price, description="", latitude=None, longitude=None, amenity_ids=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.owner_id = owner_id  # User ID of the owner
        self.price = price
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.amenity_ids = amenity_ids or []  # List of Amenity IDs

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "name": self.name,
            "owner_id": self.owner_id,
            "price": self.price,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "amenity_ids": self.amenity_ids,
        })
        return d
