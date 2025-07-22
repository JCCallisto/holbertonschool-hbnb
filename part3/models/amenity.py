from app.extensions import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
