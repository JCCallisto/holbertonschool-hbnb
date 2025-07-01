from .base import BaseEntity

class Review(BaseEntity):
    def __init__(self, text, user_id, place_id):
        super().__init__(text=text, user_id=user_id, place_id=place_id)

    def validate(self, repo):
        if not self.text or not self.text.strip():
            raise ValueError("Review text cannot be empty")
        if self.user_id not in repo.users:
            raise ValueError("user_id does not exist")
        if self.place_id not in repo.places:
            raise ValueError("place_id does not exist")
