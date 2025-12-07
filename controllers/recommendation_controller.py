# recommendation flow

from models.recommendation_engine import RecommendationEngine
from views.recommendation_view import RecommendationView


class RecommendationController:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.view = RecommendationView()
        self.engine = RecommendationEngine(user, db)
    
    def show_recommendations(self):
        filters = self.view.show_filters()
        recs = self.engine.get_recommendations(filters)
        self.view.show_recommendations(recs)