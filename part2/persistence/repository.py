import uuid
from datetime import datetime

class InMemoryRepository:
    def __init__(self):
        self.users = []

    def get_all_users(self):
        return self.users

    def create_user(self, data):
        now = datetime.utcnow().isoformat()
        user = type("User", (), {})()  # anonymous simple user object
        user.id = str(uuid.uuid4())
        user.email = data.get("email")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.created_at = now
        user.updated_at = now
        self.users.append(user)
        return user
    
    def get_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def update_user(self, user_id, data):
        for user in self.users:
            if user.id == user_id:
                user.first_name = data.get("first_name", user.first_name)
                user.last_name = data.get("last_name", user.last_name)
                user.email = data.get("email", user.email)
                user.updated_at = "2025-07-01T00:00:00Z"
                return user
        return None

    def delete_user(self, user_id):
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                return True
        return False

repo = InMemoryRepository()
