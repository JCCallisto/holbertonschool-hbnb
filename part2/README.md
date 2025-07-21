# HBnB REST API

This project is a RESTful API for the HBnB clone, built with Flask and Flask-RESTx.

## Features

- CRUD operations for Users, Places, Amenities, and Reviews
- Interactive Swagger UI for testing endpoints
- In-memory repository (no database required for this phase)

## Installation

1. **Clone the repo:**
   ```sh
   git clone https://github.com/YOUR_USERNAME/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part2
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the API:**
   ```sh
   python app.py
   ```
2. **Open Swagger UI:**  
   Go to [http://localhost:5000/](http://localhost:5000/) in your browser.

3. **Test Endpoints:**
   - Use the interactive docs to try out `POST`, `GET`, `PUT`, and `DELETE` (for reviews) for each entity.

## API Endpoints

### Users
- `GET /users/` — List users
- `POST /users/` — Create user
- `GET /users/{user_id}` — Get user by id
- `PUT /users/{user_id}` — Update user

### Amenities
- `GET /amenities/` — List amenities
- `POST /amenities/` — Create amenity
- `GET /amenities/{amenity_id}` — Get amenity by id
- `PUT /amenities/{amenity_id}` — Update amenity

### Places
- `GET /places/` — List places
- `POST /places/` — Create place
- `GET /places/{place_id}` — Get place by id
- `PUT /places/{place_id}` — Update place

### Reviews
- `GET /reviews/` — List reviews
- `POST /reviews/` — Create review
- `GET /reviews/{review_id}` — Get review by id
- `PUT /reviews/{review_id}` — Update review
- `DELETE /reviews/{review_id}` — Delete review

## Examples

### Create a User (curl)
```sh
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","first_name":"Jane","last_name":"Doe","password":"password123"}'
```

### List Amenities (curl)
```sh
curl http://localhost:5000/amenities/
```

## Notes

- All endpoints expect and return JSON.
- For detailed request/response schemas, see the Swagger UI.

## Development

- Code is organized into API, business, and persistence layers.
- To run tests:  
  *(Add this section when you have automated tests)*

## License

MIT