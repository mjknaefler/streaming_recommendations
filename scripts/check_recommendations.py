# quick check to see why recs show up

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import get_session, User, Title, Genre
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

    db.close()


if __name__ == '__main__':
    main()