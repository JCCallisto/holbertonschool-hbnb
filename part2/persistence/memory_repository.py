from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class MemoryRepository:
    def __init__(self):
        self.users = {}
        self.amenities = {}
        self.places = {}
        self.reviews = {}

    # User CRUD
    def add_user(self, user):
        self.users[user.id] = user
    def get_user(self, user_id):
        return self.users.get(user_id)
    def get_user_by_email(self, email):
        for u in self.users.values():
            if u.email == email:
                return u
        return None
    def get_all_users(self):
        return list(self.users.values())
    def update_user(self, user_id, updates):
        user = self.get_user(user_id)
        if not user:
            return None
        for k, v in updates.items():
            if k in ['first_name', 'last_name', 'email', 'password'] and v is not None:
                setattr(user, k, v)
        user.updated_at = user.updated_at.now()
        return user

    # Amenity CRUD
    def add_amenity(self, amenity):
        self.amenities[amenity.id] = amenity
    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)
    def get_amenity_by_name(self, name):
        for a in self.amenities.values():
            if a.name == name:
                return a
        return None
    def get_all_amenities(self):
        return list(self.amenities.values())
    def update_amenity(self, amenity_id, updates):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if 'name' in updates and updates['name']:
            amenity.name = updates['name']
        amenity.updated_at = amenity.updated_at.now()
        return amenity

    # Place CRUD
    def add_place(self, place):
        self.places[place.id] = place
    def get_place(self, place_id):
        return self.places.get(place_id)
    def get_all_places(self):
        return list(self.places.values())
    def update_place(self, place_id, updates):
        place = self.get_place(place_id)
        if not place:
            return None
        for k in ['title', 'description', 'price', 'latitude', 'longitude', 'amenity_ids']:
            if k in updates and updates[k] is not None:
                setattr(place, k, updates[k])
        place.updated_at = place.updated_at.now()
        return place

    # Review CRUD
    def add_review(self, review):
        self.reviews[review.id] = review
        # Link review to place
        place = self.get_place(review.place_id)
        if place:
            place.review_ids.append(review.id)
    def get_review(self, review_id):
        return self.reviews.get(review_id)
    def get_all_reviews(self):
        return list(self.reviews.values())
    def update_review(self, review_id, updates):
        review = self.get_review(review_id)
        if not review:
            return None
        for k in ['text', 'rating']:
            if k in updates and updates[k] is not None:
                setattr(review, k, updates[k])
        review.updated_at = review.updated_at.now()
        return review
    def delete_review(self, review_id):
        review = self.reviews.pop(review_id, None)
        if review:
            place = self.get_place(review.place_id)
            if place and review_id in place.review_ids:
                place.review_ids.remove(review_id)
        return review
