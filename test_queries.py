# test sqlalchemy models

from models import get_session, Title, Genre

db = get_session()

# count titles
title_count = db.query(Title).count()
print(f"Titles in database: {title_count}")

# count genres
genre_count = db.query(Genre).count()
print(f"Genres in database: {genre_count}")

# get first title if it exists
first_title = db.query(Title).first()
if first_title:
    print(f"First title: {first_title.title}")
else:
    print("No titles in database yet")

db.close()
print("\nModels are working!")