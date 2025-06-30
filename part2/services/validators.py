import re

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def validate_user_data(data):
    errors = []
    if not data.get('first_name'):
        errors.append('First name is required')
    if not data.get('last_name'):
        errors.append('Last name is required')
    email = data.get('email')
    if not email or not validate_email(email):
        errors.append('Valid email is required')
    if not data.get('password'):
        errors.append('Password is required')
    return errors

def validate_place_data(data):
    errors = []
    if not data.get('title'):
        errors.append('Title is required')
    if data.get('price') is None or not isinstance(data['price'], (float, int)) or data['price'] <= 0:
        errors.append('Price must be a positive number')
    lat = data.get('latitude')
    lon = data.get('longitude')
    if lat is None or not (-90 <= lat <= 90):
        errors.append('Latitude must be between -90 and 90')
    if lon is None or not (-180 <= lon <= 180):
        errors.append('Longitude must be between -180 and 180')
    return errors

def validate_amenity_data(data):
    errors = []
    if not data.get('name'):
        errors.append('Amenity name is required')
    return errors

def validate_review_data(data):
    errors = []
    if not data.get('text'):
        errors.append('Review text is required')
    if not data.get('user_id'):
        errors.append('user_id is required')
    if not data.get('place_id'):
        errors.append('place_id is required')
    r = data.get('rating')
    if r is None or not (1 <= r <= 5):
        errors.append('Rating must be between 1 and 5')
    return errors
