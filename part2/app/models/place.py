from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenity_ids=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []
        self.review_ids = []  # Holds IDs of reviews

    def to_dict(self, owner=None, amenities=None, reviews=None):
        d = super().to_dict()
        d['title'] = self.title
        d['description'] = self.description
        d['price'] = self.price
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude
        d['owner_id'] = self.owner_id
        d['amenity_ids'] = self.amenity_ids
        if owner is not None:
            d['owner'] = owner.to_dict() if hasattr(owner, 'to_dict') else owner
        if amenities is not None:
            d['amenities'] = [a.to_dict() for a in amenities]
        if reviews is not None:
            d['reviews'] = [r.to_dict() for r in reviews]
        return d
