import uuid
from app.models.place_amenity import place_amenity
from app.extensions import db

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'), lazy='dynamic')


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
            # Add more fields if needed
        }
