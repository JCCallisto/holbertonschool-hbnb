from business.models.user import User
from business.models.place import Place
from business.models.amenity import Amenity
from business.models.review import Review

class InMemoryRepository:
    def __init__(self):
        self.users = {}      # user_id: User
        self.places = {}     # place_id: Place
        self.amenities = {}  # amenity_id: Amenity
        self.reviews = {}    # review_id: Review

    # User CRUD
    def add_user(self, data):
        user = User(**data)
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def list_users(self):
        return list(self.users.values())

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if user:
            for key, value in data.items():
                if hasattr(user, key) and key != "password":
                    setattr(user, key, value)
            user.updated_at = user.updated_at.now()
        return user

    # Amenity CRUD
    def add_amenity(self, data):
        amenity = Amenity(**data)
        self.amenities[amenity.id] = amenity
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def list_amenities(self):
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            for key, value in data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
            amenity.updated_at = amenity.updated_at.now()
        return amenity

    # Place CRUD
    def add_place(self, data):
        place = Place(**data)
        self.places[place.id] = place
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def list_places(self):
        return list(self.places.values())

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if place:
            for key, value in data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            place.updated_at = place.updated_at.now()
        return place

    # Review CRUD
    def add_review(self, data):
        review = Review(**data)
        self.reviews[review.id] = review
        return review

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def list_reviews(self):
        return list(self.reviews.values())

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if review:
            for key, value in data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            review.updated_at = review.updated_at.now()
        return review

    def delete_review(self, review_id):
        return self.reviews.pop(review_id, None)
