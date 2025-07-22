CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);

CREATE TABLE amenity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE place (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    user_id INTEGER,
    place_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (place_id) REFERENCES place(id)
);

CREATE TABLE place_amenity (
    place_id INTEGER,
    amenity_id INTEGER,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (amenity_id) REFERENCES amenity(id)
);

-- Insert initial admin user
INSERT INTO user (email, first_name, last_name, password_hash, is_admin) VALUES (
    'admin@example.com', 'Admin', 'User', '<hashed_password>', 1
);
