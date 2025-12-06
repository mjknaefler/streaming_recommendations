# Test to see if the models work

from models import get_session, Title, Genre

# Get a database session
db = get_session()

# Test 1: Count titles
title_count = db.query(Title).count()
print(f"Titles in database: {title_count}")

# Test 2: Count genres
genre_count = db.query(Genre).count()
print(f"Genres in database: {genre_count}")

# Test 3: Try to get first title
first_title = db.query(Title).first()
if first_title:
    print(f"First title: {first_title.title}")
else:
    print("No titles in database yet")

db.close()
print("\nModels are working!")
