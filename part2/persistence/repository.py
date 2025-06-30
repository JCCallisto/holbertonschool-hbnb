from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class Repository(ABC):
    
    @abstractmethod
    def add(self, obj: Any) -> None:
        pass
    
    @abstractmethod
    def get(self, obj_id: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass
    
    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        pass
    
    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> List[Any]:
        pass

class InMemoryRepository(Repository):
    
    def __init__(self):
        self._storage: Dict[str, Any] = {}
    
    def add(self, obj: Any) -> None:
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have an 'id' attribute")
        
        self._storage[obj.id] = obj
    
    def get(self, obj_id: str) -> Optional[Any]:
        return self._storage.get(obj_id)
    
    def get_all(self) -> List[Any]:
        return list(self._storage.values())
    
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        obj = self.get(obj_id)
        if obj and hasattr(obj, 'update'):
            obj.update(data)
            return obj
        return None
    
    def delete(self, obj_id: str) -> bool:
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False
    
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> List[Any]:
        return [
            obj for obj in self._storage.values()
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value
        ]

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

user_repository = InMemoryRepository()
place_repository = InMemoryRepository()
review_repository = InMemoryRepository()
amenity_repository = InMemoryRepository()
