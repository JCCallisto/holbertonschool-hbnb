from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self, user=None, place=None):
        d = super().to_dict()
        d['text'] = self.text
        d['rating'] = self.rating
        d['place_id'] = self.place_id
        d['user_id'] = self.user_id
        if user is not None:
            d['user'] = user.to_dict() if hasattr(user, 'to_dict') else user
        if place is not None:
            d['place'] = place.to_dict() if hasattr(place, 'to_dict') else place
        return d
