from persistence.in_memory_repo import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    # -------------------- Users --------------------
    def create_user(self, data):
        return self.repo.add_user(data)

    def get_user(self, user_id):
        return self.repo.get_user(user_id)

    def list_users(self):
        return self.repo.list_users()

    def update_user(self, user_id, data):
        return self.repo.update_user(user_id, data)

    # -------------------- Amenities --------------------
    def create_amenity(self, data):
        return self.repo.add_amenity(data)

    def get_amenity(self, amenity_id):
        return self.repo.get_amenity(amenity_id)

    def list_amenities(self):
        return self.repo.list_amenities()

    def update_amenity(self, amenity_id, data):
        return self.repo.update_amenity(amenity_id, data)

    # -------------------- Places --------------------
    def create_place(self, data):
        return self.repo.add_place(data)

    def get_place(self, place_id):
        return self.repo.get_place(place_id)

    def list_places(self):
        return self.repo.list_places()

    def update_place(self, place_id, data):
        return self.repo.update_place(place_id, data)

    # -------------------- Reviews --------------------
    def create_review(self, data):
        return self.repo.add_review(data)

    def get_review(self, review_id):
        return self.repo.get_review(review_id)

    def list_reviews(self):
        return self.repo.list_reviews()

    def update_review(self, review_id, data):
        return self.repo.update_review(review_id, data)

    def delete_review(self, review_id):
        return self.repo.delete_review(review_id)
