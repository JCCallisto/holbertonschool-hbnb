from .base import BaseEntity

class Place(BaseEntity):
    def __init__(self, name, owner_id, description=None, price=None, latitude=None, longitude=None, amenity_ids=None):
        super().__init__(name=name, owner_id=owner_id, description=description, price=price, latitude=latitude, longitude=longitude)
        self.amenity_ids = amenity_ids or []
        self.review_ids = []

    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.price is not None and (not isinstance(self.price, (int, float)) or self.price < 0):
            raise ValueError("Price must be a positive number")
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
