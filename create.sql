CREATE TABLE location (
    location_id SERIAL PRIMARY KEY,
    zipcode VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    state  VARCHAR NOT NULL,
    latitude  DECIMAL NOT NULL,
    longitude  DECIMAL NOT NULL,
    population INTEGER NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password  VARCHAR NOT NULL
);

CREATE TABLE location_checkin (
    checkin_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    location_id INTEGER REFERENCES location(location_id),
    comments VARCHAR NOT NULL,
    checkin_time TIMESTAMP NOT NULL
);

/*
CREATE TABLE location_comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    location_id INTEGER REFERENCES location(location_id),
    comments VARCHAR NOT NULL
);
*/
