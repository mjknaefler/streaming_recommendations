-- drop tables if they exist
DROP TABLE IF EXISTS user_genre_preferences CASCADE;
DROP TABLE IF EXISTS user_swipes CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS title_people CASCADE;
DROP TABLE IF EXISTS people CASCADE;
DROP TABLE IF EXISTS title_country CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS title_genre CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS title CASCADE;

-- content tables
CREATE TABLE title (
    show_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    date_added DATE,
    release_year INTEGER,
    age_rating VARCHAR(20),
    duration_value INTEGER,
    duration_unit VARCHAR(20),
    description TEXT,
    CONSTRAINT check_type CHECK (type IN ('Movie', 'TV Show')),
    CONSTRAINT check_duration_unit CHECK (duration_unit IN ('min', 'Season', 'Seasons') OR duration_unit IS NULL)
);

CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE title_genre (
    show_id VARCHAR(20) NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (show_id, genre_id),
    FOREIGN KEY (show_id) REFERENCES title(show_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE title_country (
    show_id VARCHAR(20) NOT NULL,
    country_id INTEGER NOT NULL,
    PRIMARY KEY (show_id, country_id),
    FOREIGN KEY (show_id) REFERENCES title(show_id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE
);

CREATE TABLE people (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE title_people (
    show_id VARCHAR(20) NOT NULL,
    person_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,
    credit_order INTEGER,
    PRIMARY KEY (show_id, person_id, role),
    FOREIGN KEY (show_id) REFERENCES title(show_id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES people(person_id) ON DELETE CASCADE,
    CONSTRAINT check_role CHECK (role IN ('director', 'cast'))
);

-- user tables
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_username_length CHECK (LENGTH(username) >= 3)
);

CREATE TABLE user_swipes (
    swipe_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    show_id VARCHAR(20) NOT NULL,
    preference VARCHAR(20) NOT NULL,
    swiped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES title(show_id) ON DELETE CASCADE,
    CONSTRAINT unique_user_title UNIQUE (user_id, show_id),
    CONSTRAINT check_preference CHECK (preference IN ('interested', 'not_interested'))
);

CREATE TABLE user_genre_preferences (
    user_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    is_preferred BOOLEAN DEFAULT true,
    PRIMARY KEY (user_id, genre_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

-- indexes for common queries
CREATE INDEX idx_title_type ON title(type);
CREATE INDEX idx_title_release_year ON title(release_year);
CREATE INDEX idx_user_swipes_user ON user_swipes(user_id);
CREATE INDEX idx_user_swipes_preference ON user_swipes(preference);
CREATE INDEX idx_title_genre_show ON title_genre(show_id);
CREATE INDEX idx_title_genre_genre ON title_genre(genre_id);

-- trigger to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();