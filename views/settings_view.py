# settings for genre preferences

class SettingsView:
    def show_preferences(self, prefs):
        print("\n" + "-" * 40)
        print("your preferred genres:")
        if not prefs:
            print("none saved yet")
        else:
            for g in prefs:
                print(f"- {g.name}")
        print("-" * 40)

    def show_menu(self):
        print("1. add a genre")
        print("2. remove a genre")
        print("3. back to main menu")
        return input("choose an option: ").strip()

    def pick_genre(self, genres, action):
        print(f"\nchoose a genre to {action}:")
        for i, g in enumerate(genres, 1):
            print(f"{i}. {g.name}")

        choice = input("number: ").strip()
        if not choice.isdigit():
            print("not a number")
            return None

        idx = int(choice) - 1
        if idx < 0 or idx >= len(genres):
            print("not in the list")
            return None

        return genres[idx]