from typing import Dict, List, Optional, Any
from app.persistence.repository import (
    user_repository, place_repository, 
    review_repository, amenity_repository
)

class HBnBFacade:
    
    def __init__(self):
        self.user_repo = user_repository
        self.place_repo = place_repository
        self.review_repo = review_repository
        self.amenity_repo = amenity_repository
    
    def create_user(self, user_data: Dict[str, Any]) -> Any:
        from app.models.user import User
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[Any]:
        return self.user_repo.get(user_id)
    
    def get_all_users(self) -> List[Any]:
        return self.user_repo.get_all()
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[Any]:
        return self.user_repo.update(user_id, user_data)
    
    def delete_user(self, user_id: str) -> bool:
        return self.user_repo.delete(user_id)
    
    def create_place(self, place_data: Dict[str, Any]) -> Any:
        from app.models.place import Place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id: str) -> Optional[Any]:
        return self.place_repo.get(place_id)
    
    def get_all_places(self) -> List[Any]:
        return self.place_repo.get_all()
    
    def update_place(self, place_id: str, place_data: Dict[str, Any]) -> Optional[Any]:
        return self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id: str) -> bool:
        return self.place_repo.delete(place_id)
    
    def create_review(self, review_data: Dict[str, Any]) -> Any:
        from app.models.review import Review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id: str) -> Optional[Any]:
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self) -> List[Any]:
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id: str) -> List[Any]:
        return self.review_repo.get_by_attribute('place_id', place_id)
    
    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> Optional[Any]:
        return self.review_repo.update(review_id, review_data)
    
    def delete_review(self, review_id: str) -> bool:
        return self.review_repo.delete(review_id)
    
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Any:
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id: str) -> Optional[Any]:
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self) -> List[Any]:
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id: str, amenity_data: Dict[str, Any]) -> Optional[Any]:
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id: str) -> bool:
        return self.amenity_repo.delete(amenity_id)

facade = HBnBFacade()
