from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.users = {}
        self.amenities = {}
        self.places = {}
        self.reviews = {}

    def create_user(self, user_data):
        email = user_data.get('email', '').strip().lower()
        for user in self.users.values():
            if user.email == email:
                raise ValueError("Email already exists")
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_all_users(self):
        return list(self.users.values())

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        
        if 'email' in user_data:
            email = user_data['email'].strip().lower()
            for uid, u in self.users.items():
                if uid != user_id and u.email == email:
                    raise ValueError("Email already exists")
        
        user.update(user_data)
        return user

    def create_amenity(self, amenity_data):
        name = amenity_data.get('name', '').strip()
        for amenity in self.amenities.values():
            if amenity.name.lower() == name.lower():
                raise ValueError("Amenity name already exists")
        
        amenity = Amenity(name=amenity_data['name'])
        self.amenities[amenity.id] = amenity
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data:
            name = amenity_data['name'].strip()
            for aid, a in self.amenities.items():
                if aid != amenity_id and a.name.lower() == name.lower():
                    raise ValueError("Amenity name already exists")
        
        amenity.update(amenity_data)
        return amenity

    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        amenity_ids = place_data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            if not self.get_amenity(amenity_id):
                raise ValueError(f"Amenity {amenity_id} not found")
        
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id'],
            facade=self  # Pass facade reference to avoid circular imports
        )
        
        # Add amenities to place
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            place.add_amenity(amenity)
        
        self.places[place.id] = place
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def get_all_places(self):
        return list(self.places.values())

    def get_place_with_details(self, place_id):
        return self.get_place(place_id)

    def get_all_places_with_details(self):
        return self.get_all_places()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        if 'amenity_ids' in place_data:
            amenity_ids = place_data['amenity_ids']
            for amenity_id in amenity_ids:
                if not self.get_amenity(amenity_id):
                    raise ValueError(f"Amenity {amenity_id} not found")
            
            # Clear current amenities and add new ones
            place._amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                place.add_amenity(amenity)
        
        place.update(place_data)
        return place

    def create_review(self, review_data):
        # Validate place and user exist
        place = self.get_place(review_data['place_id'])
        user = self.get_user(review_data['user_id'])
        
        if not place:
            raise ValueError("Place not found")
        if not user:
            raise ValueError("User not found")
        
        # Check if user is trying to review their own place
        if user.id == place.owner_id:
            raise ValueError("Users cannot review their own places")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id'],
            facade=self  # Pass facade reference
        )
        
        self.reviews[review.id] = review
        return review

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return list(self.reviews.values())

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.reviews.pop(review_id, None)
        if review:
            # Remove review from place and user
            place = self.get_place(review.place_id)
            user = self.get_user(review.user_id)
            
            if place:
                place.remove_review(review)
            if user:
                user.remove_review(review)
        
        return review is not None
    facade = HBnBFacade()
