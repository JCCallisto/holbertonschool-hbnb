from app.persistence.memory_repository import MemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services import validators

class HBnBFacade:
    def __init__(self):
        self.repo = MemoryRepository()

    # User
    def create_user(self, data):
        errors = validators.validate_user_data(data)
        if errors:
            raise ValueError("; ".join(errors))
        if self.repo.get_user_by_email(data['email']):
            raise ValueError("Email already exists")
        user = User(data['first_name'], data['last_name'], data['email'], data['password'], data.get('is_admin', False))
        self.repo.add_user(user)
        return user

    def get_user(self, user_id):
        return self.repo.get_user(user_id)

    def get_all_users(self):
        return self.repo.get_all_users()

    def update_user(self, user_id, data):
        errors = validators.validate_user_data({**self.repo.get_user(user_id).__dict__, **data})
        if errors:
            raise ValueError("; ".join(errors))
        if 'email' in data:
            existing = self.repo.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already exists")
        return self.repo.update_user(user_id, data)

    # Amenity
    def create_amenity(self, data):
        errors = validators.validate_amenity_data(data)
        if errors:
            raise ValueError("; ".join(errors))
        if self.repo.get_amenity_by_name(data['name']):
            raise ValueError("Amenity name already exists")
        amenity = Amenity(data['name'])
        self.repo.add_amenity(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.repo.get_amenity(amenity_id)

    def get_all_amenities(self):
        return self.repo.get_all_amenities()

    def update_amenity(self, amenity_id, data):
        errors = validators.validate_amenity_data({**self.repo.get_amenity(amenity_id).__dict__, **data})
        if errors:
            raise ValueError("; ".join(errors))
        if 'name' in data:
            existing = self.repo.get_amenity_by_name(data['name'])
            if existing and existing.id != amenity_id:
                raise ValueError("Amenity name already exists")
        return self.repo.update_amenity(amenity_id, data)

    # Place
    def create_place(self, data):
        errors = validators.validate_place_data(data)
        if errors:
            raise ValueError("; ".join(errors))
        if not self.repo.get_user(data['owner_id']):
            raise ValueError("Owner not found")
        for amenity_id in data.get('amenity_ids', []):
            if not self.repo.get_amenity(amenity_id):
                raise ValueError("Amenity not found: " + amenity_id)
        place = Place(
            data['title'], data.get('description', ""), data['price'],
            data['latitude'], data['longitude'], data['owner_id'], data.get('amenity_ids', []))
        self.repo.add_place(place)
        return place

    def get_place(self, place_id):
        return self.repo.get_place(place_id)

    def get_all_places(self):
        return self.repo.get_all_places()

    def update_place(self, place_id, data):
        errors = validators.validate_place_data({**self.repo.get_place(place_id).__dict__, **data})
        if errors:
            raise ValueError("; ".join(errors))
        if 'owner_id' in data:
            if not self.repo.get_user(data['owner_id']):
                raise ValueError("Owner not found")
        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not self.repo.get_amenity(amenity_id):
                    raise ValueError("Amenity not found: " + amenity_id)
        return self.repo.update_place(place_id, data)

    # For serialization with relations
    def get_place_with_details(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        owner = self.get_user(place.owner_id)
        amenities = [self.get_amenity(aid) for aid in place.amenity_ids if self.get_amenity(aid)]
        reviews = [self.get_review(rid) for rid in getattr(place, 'review_ids', []) if self.get_review(rid)]
        return place, owner, amenities, reviews

    def get_all_places_with_details(self):
        return [self.get_place_with_details(p.id) for p in self.get_all_places()]

    # Review
    def create_review(self, data):
        errors = validators.validate_review_data(data)
        if errors:
            raise ValueError("; ".join(errors))
        if not self.repo.get_place(data['place_id']):
            raise ValueError("Place not found")
        if not self.repo.get_user(data['user_id']):
            raise ValueError("User not found")
        review = Review(data['text'], data['rating'], data['place_id'], data['user_id'])
        self.repo.add_review(review)
        return review

    def get_review(self, review_id):
        return self.repo.get_review(review_id)

    def get_all_reviews(self):
        return self.repo.get_all_reviews()

    def update_review(self, review_id, data):
        errors = validators.validate_review_data({**self.repo.get_review(review_id).__dict__, **data})
        if errors:
            raise ValueError("; ".join(errors))
        return self.repo.update_review(review_id, data)

    def delete_review(self, review_id):
        return self.repo.delete_review(review_id)
