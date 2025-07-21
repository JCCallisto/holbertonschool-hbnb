from .base import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, text, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id      # Reviewer (User ID)
        self.place_id = place_id    # Place being reviewed
        self.text = text

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": self.text,
        })
        return d
