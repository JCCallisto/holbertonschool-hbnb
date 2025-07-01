from persistence.repository import repo

class HBNBFacade:
    def list_users(self):
        users = repo.get_all_users()
        return [self._serialize_user(user) for user in users]

    def create_user(self, data):
        user = repo.create_user(data)
        return self._serialize_user(user)

    def update_user(self, user_id, data):
        user = repo.update_user(user_id, data)
        return self._serialize_user(user)

    def delete_user(self, user_id):
        return repo.delete_user(user_id)
    
    def get_user(self, user_id):
        user = repo.get_user(user_id)
        if user:
            return self._serialize_user(user)
        return None

    def _serialize_user(self, user):
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

hbnb_facade = HBNBFacade()
