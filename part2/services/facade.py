"""
HBnB Facade Service - Business Logic Layer
Handles all business operations and coordinates between models and repositories
"""
from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    """
    Facade pattern implementation for HBnB application
    Provides a simplified interface to the complex subsystem of models
    """
    
    def __init__(self):
        # In-memory storage (replace with actual database in production)
        self._users = {}
        self._places = {}
        self._amenities = {}
        self._reviews = {}
    
    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        # Validate email uniqueness
        email = user_data.get('email')
        if any(u.email == email for u in self._users.values()):
            raise ValueError(f"User with email {email} already exists")
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"{field} is required")
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        self._users[user.id] = user
        return user
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self._users.get(user_id)
    
    def get_all_users(self):
        """Get all users"""
        return list(self._users.values())
    
    def update_user(self, user_id, user_data):
        """Update user"""
        user = self._users.get(user_id)
        if not user:
            return None
        
        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            if any(u.email == user_data['email'] for u in self._users.values()):
                raise ValueError(f"User with email {user_data['email']} already exists")
        
        # Update fields
        for field in ['first_name', 'last_name', 'email', 'password']:
            if field in user_data:
                setattr(user, field, user_data[field])
        
        user.updated_at = datetime.utcnow()
        return user
    
    # Amenity operations
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Name is required")
        
        # Check name uniqueness
        if any(a.name == name for a in self._amenities.values()):
            raise ValueError(f"Amenity with name '{name}' already exists")
        
        amenity = Amenity(name=name)
        self._amenities[amenity.id] = amenity
        return amenity
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self._amenities.get(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return list(self._amenities.values())
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity"""
        amenity = self._amenities.get(amenity_id)
        if not amenity:
            return None
        
        name = amenity_data.get('name')
        if name and name != amenity.name:
            # Check name uniqueness
            if any(a.name == name for a in self._amenities.values()):
                raise ValueError(f"Amenity with name '{name}' already exists")
            amenity.name = name
            amenity.updated_at = datetime.utcnow()
        
        return amenity
    
    # Place operations
    def create_place(self, place_data):
        """Create a new place"""
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"{field} is required")
        
        # Validate owner exists
        owner_id = place_data['owner_id']
        if owner_id not in self._users:
            raise ValueError(f"Owner with ID {owner_id} not found")
        
        # Validate amenities exist
        amenity_ids = place_data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            if amenity_id not in self._amenities:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner_id,
            amenity_ids=amenity_ids
        )
        self._places[place.id] = place
        return place
    
    def get_place(self, place_id):
        """Get place by ID"""
        return self._places.get(place_id)
    
    def get_place_with_details(self, place_id):
        """Get place with owner, amenities, and reviews"""
        place = self._places.get(place_id)
        if not place:
            return None
        
        owner = self._users.get(place.owner_id)
        amenities = [self._amenities[aid] for aid in place.amenity_ids if aid in self._amenities]
        reviews = [r for r in self._reviews.values() if r.place_id == place_id]
        
        return place, owner, amenities, reviews
    
    def get_all_places(self):
        """Get all places"""
        return list(self._places.values())
    
    def get_all_places_with_details(self):
        """Get all places with details"""
        results = []
        for place in self._places.values():
            owner = self._users.get(place.owner_id)
            amenities = [self._amenities[aid] for aid in place.amenity_ids if aid in self._amenities]
            reviews = [r for r in self._reviews.values() if r.place_id == place.id]
            results.append((place, owner, amenities, reviews))
        return results
    
    def update_place(self, place_id, place_data):
        """Update place"""
        place = self._places.get(place_id)
        if not place:
            return None
        
        # Validate amenities if provided
        if 'amenity_ids' in place_data:
            for amenity_id in place_data['amenity_ids']:
                if amenity_id not in self._amenities:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Update fields
        updatable_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'amenity_ids']
        for field in updatable_fields:
            if field in place_data:
                setattr(place, field, place_data[field])
        
        place.updated_at = datetime.utcnow()
        return place
    
    # Review operations
    def create_review(self, review_data):
        """Create a new review"""
        # Validate required fields
        required_fields = ['text', 'rating', 'place_id', 'user_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"{field} is required")
        
        # Validate place exists
        place_id = review_data['place_id']
        if place_id not in self._places:
            raise ValueError(f"Place with ID {place_id} not found")
        
        # Validate user exists
        user_id = review_data['user_id']
        if user_id not in self._users:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Validate rating range
        rating = review_data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        review = Review(
            text=review_data['text'],
            rating=rating,
            place_id=place_id,
            user_id=user_id
        )
        self._reviews[review.id] = review
        return review
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self._reviews.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return list(self._reviews.values())
    
    def update_review(self, review_id, review_data):
        """Update review"""
        review = self._reviews.get(review_id)
        if not review:
            return None
        
        # Validate rating if provided
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Update fields
        updatable_fields = ['text', 'rating']
        for field in updatable_fields:
            if field in review_data:
                setattr(review, field, review_data[field])
        
        review.updated_at = datetime.utcnow()
        return review
    
    def delete_review(self, review_id):
        """Delete review"""
        review = self._reviews.get(review_id)
        if review:
            del self._reviews[review_id]
        return review
