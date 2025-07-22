from app.models.user import User
from app.extensions import db

class UserRepository:
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def create(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
