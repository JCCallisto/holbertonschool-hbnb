from app.models.base_model import BaseModel
from app.models.user import OwnerMixin

class Place(OwnerMixin, BaseModel):
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__(owner_id)
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self._amenities = []
        self._reviews = []
    
    def _validate_title(self, title):
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title.strip()
    
    def _validate_description(self, description):
        if description is None:
            return ""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        return description.strip()
    
    def _validate_price(self, price):
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return float(price)
    
    def _validate_latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)
    
    def _validate_longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)
    
    def add_amenity(self, amenity):
        from app.services.facade import facade
        if isinstance(amenity, str):
            amenity_obj = facade.get_amenity(amenity)
            if not amenity_obj:
                raise ValueError("Amenity not found")
            amenity = amenity_obj
        
        if amenity not in self._amenities:
            self._amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        from app.services.facade import facade
        if isinstance(amenity, str):
            amenity_obj = facade.get_amenity(amenity)
            if amenity_obj:
                amenity = amenity_obj
        
        if amenity in self._amenities:
            self._amenities.remove(amenity)
    
    def add_review(self, review):
        if review not in self._reviews:
            self._reviews.append(review)
    
    def remove_review(self, review):
        if review in self._reviews:
            self._reviews.remove(review)
    
    @property
    def amenities(self):
        return self._amenities.copy()
    
    @property
    def reviews(self):
        return self._reviews.copy()
    
    @property
    def average_rating(self):
        if not self._reviews:
            return 0.0
        total_rating = sum(review.rating for review in self._reviews)
        return round(total_rating / len(self._reviews), 2)
    
    def update(self, data):
        if 'title' in data:
            self.title = self._validate_title(data['title'])
        if 'description' in data:
            self.description = self._validate_description(data['description'])
        if 'price' in data:
            self.price = self._validate_price(data['price'])
        if 'latitude' in data:
            self.latitude = self._validate_latitude(data['latitude'])
        if 'longitude' in data:
            self.longitude = self._validate_longitude(data['longitude'])
        super().save()
    
    def to_dict(self, include_owner=False, include_amenities=False, include_reviews=False):
        """Convert place to dictionary with optional detailed information"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        
        if include_owner and hasattr(self, '_owner') and self._owner:
            data['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        
        if include_amenities:
            data['amenities'] = [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in self._amenities
            ]
        else:
            data['amenity_ids'] = [amenity.id for amenity in self._amenities]
        
        if include_reviews:
            data['reviews'] = [review.to_dict() for review in self._reviews]
            data['average_rating'] = self.average_rating
        else:
            data['review_count'] = len(self._reviews)
            data['average_rating'] = self.average_rating
        
        return data
    
    def __repr__(self):
        return f"<Place {self.id}: {self.title} (${self.price})>"
