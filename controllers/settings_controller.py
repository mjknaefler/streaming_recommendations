# manage user genre preferences

from models import Genre, UserGenrePreference
from views.settings_view import SettingsView

class SettingsController:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.view = SettingsView()

    def manage_preferences(self):
        while True:
            prefs = self.get_current_preferences()
            self.view.show_preferences(prefs)
            choice = self.view.show_menu()

            if choice == '1':
                self.add_preference()
            elif choice == '2':
                self.remove_preference()
            elif choice == '3':
                break
            else:
                print("not an option, try again")

    def get_current_preferences(self):
        q = self.db.query(Genre)
        q = q.join(UserGenrePreference, UserGenrePreference.genre_id == Genre.genre_id)
        q = q.filter(UserGenrePreference.user_id == self.user.user_id)
        q = q.filter(UserGenrePreference.is_preferred == True)
        q = q.order_by(Genre.name)
        return q.all()

    def get_available_genres(self):
        preferred_ids = self.db.query(UserGenrePreference.genre_id).filter(
            UserGenrePreference.user_id == self.user.user_id,
            UserGenrePreference.is_preferred == True,
        )

        q = self.db.query(Genre)
        q = q.filter(~Genre.genre_id.in_(preferred_ids))
        q = q.order_by(Genre.name)
        return q.all()

    def add_preference(self):
        available = self.get_available_genres()
        if not available:
            print("all genres already saved")
            return

        genre = self.view.pick_genre(available, "add")
        if not genre:
            return

        pref = self.db.query(UserGenrePreference).filter(
            UserGenrePreference.user_id == self.user.user_id,
            UserGenrePreference.genre_id == genre.genre_id,
        ).first()

        if pref:
            if pref.is_preferred:
                print("already saved")
                return
            pref.is_preferred = True
        else:
            pref = UserGenrePreference(user_id=self.user.user_id, genre_id=genre.genre_id, is_preferred=True)
            self.db.add(pref)

        self.db.commit()
        print(f"saved {genre.name} as preferred")

    def remove_preference(self):
        prefs = self.get_current_preferences()
        if not prefs:
            print("no genres to remove")
            return

        genre = self.view.pick_genre(prefs, "remove")
        if not genre:
            return

        pref = self.db.query(UserGenrePreference).filter(
            UserGenrePreference.user_id == self.user.user_id,
            UserGenrePreference.genre_id == genre.genre_id,
            UserGenrePreference.is_preferred == True,
        ).first()

        pref.is_preferred = False
        self.db.commit()
        print(f"removed {genre.name}")