# quick check to see why recs show up

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import get_session, User, Genre
from models.recommendation_engine import RecommendationEngine


def show_swipe_genres(engine, db):
    if not engine.interested_genres:
        print("no interested swipes yet")
        return
    print("\ntop genres from interested swipes:")
    for genre_id, count in sorted(engine.interested_genres.items(), key=lambda x: x[1], reverse=True):
        name = db.query(Genre.name).filter(Genre.genre_id == genre_id).first()[0]
        print(f"- {name}: {count}")


def show_pref_genres(engine, db):
    if not engine.pref_genres:
        print("no saved genre prefs yet")
        return
    print("\nsaved genre prefs:")
    for genre_id in engine.pref_genres:
        name = db.query(Genre.name).filter(Genre.genre_id == genre_id).first()[0]
        print(f"- {name}")


def show_sample_recs(engine, limit=10):
    recs = engine.get_recommendations()
    if not recs:
        print("\nno recs. swipe more and try again")
        return
    print("\nsample recommendations (score + title)")
    for score, title in recs[:limit]:
        genres = ", ".join([g.name for g in title.genres])
        print(f"{score} - {title.title} ({title.type}, {title.release_year})")
        print(f"   genres: {genres}")

def show_score_check(engine):
    if not engine.interested_genres and not engine.pref_genres and not engine.top_type:
        print("\nno data to score yet")
        return

    recs = engine.get_recommendations()
    if not recs:
        print("\nre-run after swiping more titles")
        return

    score, title = recs[0]

    genres = [g.genre_id for g in title.genres]
    if genres:
        matches = sum(1 for g in genres if g in engine.interested_genres)
        pref_matches = sum(1 for g in genres if g in engine.pref_genres)
        genre_match_score = matches / len(genres)
        preference_score = pref_matches / len(genres)
    else:
        genre_match_score = 0
        preference_score = 0

    if engine.top_type and title.type.lower() == engine.top_type.lower():
        type_score = 1.0
    else:
        type_score = 0.5

    weighted_genre = round(genre_match_score * engine.swipe_weight, 4)
    weighted_pref = round(preference_score * engine.pref_weight, 4)
    weighted_type = round(type_score * engine.type_weight, 4)

    print("\nscore breakdown for top rec:")
    print(f"- title: {title.title} ({title.type})")
    print(f"- genre match score: {genre_match_score} -> {weighted_genre}")
    print(f"- pref match score: {preference_score} -> {weighted_pref}")
    print(f"- type score: {type_score} -> {weighted_type}")
    print(f"- combined: {weighted_genre + weighted_pref + weighted_type} (engine score: {score})")
    print(f"- weight sum: {engine.swipe_weight + engine.pref_weight + engine.type_weight}")


def main():
    username = input("username: ").strip().lower()
    db = get_session()

    user = db.query(User).filter(User.username == username).first()
    if not user:
        print("user not found")
        db.close()
        return

    engine = RecommendationEngine(user, db)
    engine.load_user_data()

    print("\nweights:")
    print(f"- swipe weight: {engine.swipe_weight}")
    print(f"- pref weight: {engine.pref_weight}")
    print(f"- type weight: {engine.type_weight}")
    print(f"- top type: {engine.top_type}")

    show_swipe_genres(engine, db)
    show_pref_genres(engine, db)
    show_sample_recs(engine)
    show_score_check(engine)

    db.close()


if __name__ == '__main__':
    main()