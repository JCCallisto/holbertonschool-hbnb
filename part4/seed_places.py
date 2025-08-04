from app import create_app
from app.extensions import db
from app.models.place import Place
from app.models.user import User  # Needed for owner_id

app = create_app("DevelopmentConfig")  # use your real config name

with app.app_context():
    # Get any user to be the owner/host
    owner = User.query.first()
    if not owner:
        print("No user found. Please create a user first!")
        exit(1)

    place1 = Place(
        name="Beautiful Beach House",
        price=150.0,
        description="A beautiful beach house with amazing views...",
        location="Miami, USA",
        latitude=25.7617,
        longitude=-80.1918,
        owner_id=owner.id
    )
    place2 = Place(
        name="Cozy Cabin",
        price=100.0,
        description="A cozy cabin in the mountains.",
        location="Aspen, USA",
        latitude=39.1911,
        longitude=-106.8175,
        owner_id=owner.id
    )
    place3 = Place(
        name="Modern Apartment",
        price=200.0,
        description="A modern apartment in the city center.",
        location="New York, USA",
        latitude=40.7128,
        longitude=-74.0060,
        owner_id=owner.id
    )

    db.session.add_all([place1, place2, place3])
    db.session.commit()
    print("Sample places added!")