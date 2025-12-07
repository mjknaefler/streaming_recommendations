# Load Netflix data

import pandas as pd
from models import get_session, Title, Genre, Country, People, TitleGenre, TitleCountry, TitlePeople

# Path to the CSV file
CSV_FILE = 'netflix_titles.csv'

def load_csv():
    print(f"Loading {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded {len(df)} records")
    return df

def add_genres(db, df):
    print("Adding genres...")
    # Get unique genres
    genres = set()
    for listed_in in df['listed_in'].dropna():
        for genre in listed_in.split(','):
            genres.add(genre.strip())
    
    genre_map = {}
    for genre_name in sorted(genres):
        genre = Genre(name=genre_name)
        db.add(genre)
        db.flush()
        genre_map[genre_name] = genre.genre_id
    
    db.commit()
    print(f"Added {len(genre_map)} genres")
    return genre_map

def add_countries(db, df):
    print("Adding countries...")
    countries = set()
    for country_str in df['country'].dropna():
        for country in country_str.split(','):
            countries.add(country.strip())
    
    country_map = {}
    for country_name in sorted(countries):
        country = Country(name=country_name)
        db.add(country)
        db.flush()
        country_map[country_name] = country.country_id
    
    db.commit()
    print(f"Added {len(country_map)} countries")
    return country_map

def add_people(db, df):
    print("Adding people (directors and cast)...")
    people = set()
    
    # Get directors
    for director_str in df['director'].dropna():
        for director in director_str.split(','):
            people.add(director.strip())
    
    # Get cast
    for cast_str in df['cast'].dropna():
        for person in cast_str.split(','):
            people.add(person.strip())
    
    people_map = {}
    for person_name in sorted(people):
        person = People(name=person_name)
        db.add(person)
        db.flush()
        people_map[person_name] = person.person_id
    
    db.commit()
    print(f"Added {len(people_map)} people")
    return people_map

def add_titles(db, df, genre_map, country_map, people_map):
    print("Adding titles...")
    count = 0
    
    for idx, row in df.iterrows():
        try:
            # Parse duration
            duration_val = None
            duration_unit = None
            if pd.notna(row['duration']):
                parts = row['duration'].split()
                if len(parts) >= 2:
                    duration_val = int(parts[0])
                    duration_unit = parts[1]
            
            # Parse date
            date_val = pd.to_datetime(row['date_added'], errors='coerce')
            date_added = date_val.date() if pd.notna(date_val) else None
            
            # Create title
            title = Title(
                show_id=row['show_id'],
                title=row['title'],
                type=row['type'],
                date_added=date_added,
                release_year=int(row['release_year']) if pd.notna(row['release_year']) else None,
                age_rating=row['rating'] if pd.notna(row['rating']) else 'Not Rated',
                duration_value=duration_val,
                duration_unit=duration_unit,
                description=row['description'] if pd.notna(row['description']) else ''
            )
            db.add(title)
            db.flush()
            
            # Add genres
            if pd.notna(row['listed_in']):
                for genre in row['listed_in'].split(','):
                    genre = genre.strip()
                    if genre in genre_map:
                        db.add(TitleGenre(show_id=row['show_id'], genre_id=genre_map[genre]))
            
            # Add countries
            if pd.notna(row['country']):
                for country in row['country'].split(','):
                    country = country.strip()
                    if country in country_map:
                        db.add(TitleCountry(show_id=row['show_id'], country_id=country_map[country]))
            
            # Add directors (skip duplicates)
            if pd.notna(row['director']):
                seen_directors = set()
                for i, director in enumerate(row['director'].split(',')):
                    director = director.strip()
                    if director in people_map and director not in seen_directors:
                        db.add(TitlePeople(
                            show_id=row['show_id'],
                            person_id=people_map[director],
                            role='director',
                            credit_order=i
                        ))
                        seen_directors.add(director)
            
            # Add cast (skip duplicates)
            if pd.notna(row['cast']):
                seen_cast = set()
                for i, person in enumerate(row['cast'].split(',')):
                    person = person.strip()
                    if person in people_map and person not in seen_cast:
                        db.add(TitlePeople(
                            show_id=row['show_id'],
                            person_id=people_map[person],
                            role='cast',
                            credit_order=i
                        ))
                        seen_cast.add(person)
            
            # Commit every 100 records
            if (idx + 1) % 100 == 0:
                db.commit()
                print(f"  Processed {idx + 1} titles...")
            
            count += 1
        
        except Exception as e:
            print(f"Error on row {idx}: {e}")
            db.rollback()
    
    db.commit()
    print(f"Added {count} titles")

def main():
    print("=" * 50)
    print("Loading Netflix data into database")
    print("=" * 50)
    
    df = load_csv()
    db = get_session()
    
    try:
        genre_map = add_genres(db, df)
        country_map = add_countries(db, df)
        people_map = add_people(db, df)
        add_titles(db, df, genre_map, country_map, people_map)
        
        print("\nDone! Data loaded successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
