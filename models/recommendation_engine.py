# recommendation scoring
from sqlalchemy import func, and_
from models import Title, Genre, TitleGenre, UserSwipe, UserGenrePreference


class RecommendationEngine:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.interested_genres = None
        self.pref_genres = None
        self.top_type = None
        self.swipe_weight = 0.6
        self.pref_weight = 0.3
        self.type_weight = 0.1
    
    def load_user_data(self):
        # genres from interested swipes
        q = self.db.query(Genre.genre_id, func.count(Genre.genre_id))
        q = q.join(TitleGenre, Genre.genre_id == TitleGenre.genre_id)
        q = q.join(Title, Title.show_id == TitleGenre.show_id)
        q = q.join(UserSwipe, and_(UserSwipe.show_id == Title.show_id, UserSwipe.user_id == self.user.user_id))
        q = q.filter(UserSwipe.preference == 'interested')
        q = q.group_by(Genre.genre_id)
        genre_counts = q.all()
        self.interested_genres = {g_id: count for g_id, count in genre_counts}

        # genre preferences
        prefs_q = self.db.query(UserGenrePreference.genre_id)
        prefs_q = prefs_q.filter(UserGenrePreference.user_id == self.user.user_id)
        prefs_q = prefs_q.filter(UserGenrePreference.is_preferred == True)
        prefs = prefs_q.all()
        self.pref_genres = set(g_id for g_id, in prefs)

        # top content type from swipes
        type_q = self.db.query(Title.type, func.count(Title.type))
        type_q = type_q.join(UserSwipe, and_(UserSwipe.show_id == Title.show_id, UserSwipe.user_id == self.user.user_id))
        type_q = type_q.group_by(Title.type)
        type_counts = type_q.all()
        if type_counts:
            self.top_type = sorted(type_counts, key=lambda x: x[1], reverse=True)[0][0]
        else:
            self.top_type = None

        # light weighting so swipes matter most, shift more to type if preferences are empty
        if self.interested_genres:
            self.swipe_weight = 0.6
        else:
            self.swipe_weight = 0.4

        if self.pref_genres:
            self.pref_weight = 0.25
        else:
            self.pref_weight = 0.15

        # whatever is left goes to type just so it adds up to 1
        self.type_weight = max(0, 1 - (self.swipe_weight + self.pref_weight))

    def get_candidates(self, filters=None):
        filters = filters or {}
        q = self.db.query(Title)
        q = q.outerjoin(UserSwipe, and_(UserSwipe.show_id == Title.show_id, UserSwipe.user_id == self.user.user_id))
        q = q.filter(UserSwipe.swipe_id == None)

        if filters.get('type'):
            q = q.filter(Title.type.ilike(filters['type']))
        if filters.get('year_min'):
            q = q.filter(Title.release_year >= filters['year_min'])
        if filters.get('year_max'):
            q = q.filter(Title.release_year <= filters['year_max'])
        if filters.get('rating'):
            q = q.filter(Title.age_rating == filters['rating'])

        # don't fetch all titles at once
        return q.limit(200).all()  

    def score_title(self, title):
        genres = [g.genre_id for g in title.genres]
        if not genres:
            genre_match_score = 0
            preference_score = 0
        else:
            matches = sum(1 for g in genres if g in self.interested_genres)
            pref_matches = sum(1 for g in genres if g in self.pref_genres)
            genre_match_score = matches / len(genres) if genres else 0
            preference_score = pref_matches / len(genres) if genres else 0
        
        if self.top_type and title.type.lower() == self.top_type.lower():
            type_score = 1.0
        else:
            type_score = 0.5

        total = (genre_match_score * self.swipe_weight) + (preference_score * self.pref_weight) + (type_score * self.type_weight)
        return round(total, 4)
    
    def get_recommendations(self, filters=None):
        self.load_user_data()
        candidates = self.get_candidates(filters)
        scored = []
        for title in candidates:
            score = self.score_title(title)
            scored.append((score, title))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:20]