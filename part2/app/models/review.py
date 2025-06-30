from app.models.base_model import BaseModel

class Review(BaseModel):
    
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place_id = self._validate_place_id(place_id)
        self.user_id = self._validate_user_id(user_id)
        
        self._setup_relationships()
    
    def _validate_text(self, text):
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        if len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 1000:
            raise ValueError("Review text cannot exceed 1000 characters")
        return text.strip()
    
    def _validate_rating(self, rating):
        if not isinstance(rating, (int, float)):
            raise ValueError("Rating must be a number")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return int(rating)
    
    def _validate_place_id(self, place_id):
        from app.services.facade import facade
        if not place_id:
            raise ValueError("Place ID is required")
        place = facade.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place_id
    
    def _validate_user_id(self, user_id):
        from app.services.facade import facade
        if not user_id:
            raise ValueError("User ID is required")
        user = facade.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        place = facade.get_place(self.place_id)
        if place and user.id == place.owner_id:
            raise ValueError("Users cannot review their own places")
        
        return user_id
    
    def _setup_relationships(self):
        from app.services.facade import facade
        place = facade.get_place(self.place_id)
        user = facade.get_user(self.user_id)
        
        if place:
            place.add_review(self)
            self._place = place
        
        if user:
            user.add_review(self)
            self._user = user
    
    @property
    def place(self):
        return self._place
    
    @property
    def user(self):
        return self._user
    
    def update(self, data):
        if 'text' in data:
            self.text = self._validate_text(data['text'])
        if 'rating' in data:
            self.rating = self._validate_rating(data['rating'])
        super().save()
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            },
            'place': {
                'id': self.place.id,
                'title': self.place.title
            }
        })
        return data
    
    def __repr__(self):
        return f"<Review {self.id}: {self.rating}/5 stars for {self.place.title}>"
