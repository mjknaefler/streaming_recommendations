# main application controller

from models import get_session, User, UserSwipe
from views.menu_view import MenuView

class MainController:
    def __init__(self):
        self.db = get_session()
        self.current_user = None
        self.menu_view = MenuView()
    
    def run(self):
        # get or create user
        self.setup_user()
        
        # main loop
        while True:
            choice = self.menu_view.show_menu()
            
            if choice == '1':
                # swipe interface
                from controllers.swipe_controller import SwipeController
                swipe = SwipeController(self.current_user, self.db)
                swipe.start_swiping()
            
            elif choice == '2':
                # view recommendations
                from controllers.recommendation_controller import RecommendationController
                rec = RecommendationController(self.current_user, self.db)
                rec.show_recommendations()
            
            elif choice == '3':
                # settings
                from controllers.settings_controller import SettingsController
                settings = SettingsController(self.current_user, self.db)
                settings.manage_preferences()
            
            elif choice == '4':
                # exit
                print("\nThanks for using the app!")
                self.db.close()
                break
            
            else:
                print("Invalid choice. Try again.")
    
    def setup_user(self):
        print("\nWelcome!")
        username = input("Enter your username: ").strip().lower()
        
        # check if user exists
        user = self.db.query(User).filter(User.username == username).first()
        
        if user:
            print(f"\nWelcome back, {username}!")
            # show some stats
            swipe_count = self.db.query(UserSwipe).filter(UserSwipe.user_id == user.user_id).count()
            print(f"You have {swipe_count} previous swipes.")
            self.current_user = user
        else:
            # create new user
            print(f"\nNew user! Creating profile for {username}...")
            user = User(username=username)
            self.db.add(user)
            self.db.commit()
            print("Profile created!")
            self.current_user = user
