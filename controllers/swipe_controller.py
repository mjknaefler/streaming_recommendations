# handle swipe flow

from sqlalchemy import and_, func

from models import Title, UserSwipe
from views.swipe_view import SwipeView


class SwipeController:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.view = SwipeView()
        self.buffer = []

    def start_swiping(self):
        print("\nloading titles...")
        self.load_more_titles()
        if not self.buffer:
            self.view.no_titles_left()
            return

        while True:
            if not self.buffer:
                self.load_more_titles()
                if not self.buffer:
                    self.view.no_titles_left()
                    break
            title = self.buffer.pop()
            self.view.show_title(title)
            choice = self.view.get_choice()
            
            if choice == 'x':
                print("\nback to main menu")
                break
            elif choice == 'y':
                self.save_swipe(title, 'interested')
                print("saved as interested")
            elif choice == 'n':
                self.save_swipe(title, 'not_interested')
                print("saved as not interested")

    def load_more_titles(self, batch_size=10):
        # get random titles user hasn't swiped on
        q = self.db.query(Title)
        q = q.outerjoin(UserSwipe, and_(UserSwipe.show_id == Title.show_id, UserSwipe.user_id == self.user.user_id))
        q = q.filter(UserSwipe.swipe_id == None)
        q = q.order_by(func.random())
        # grab a handful at a time
        q = q.limit(batch_size)  
        titles = q.all()
        self.buffer.extend(titles)

    def save_swipe(self, title, preference):
        # save decision
        swipe = UserSwipe(
            user_id=self.user.user_id,
            show_id=title.show_id,
            preference=preference
        )
        self.db.add(swipe)
        try:
            self.db.commit()
        except Exception as e:
            print(f"error saving swipe: {e}")
            self.db.rollback()