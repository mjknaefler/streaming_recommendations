# display main menu

class MenuView:
    def show_menu(self):
        print("\n" + "=" * 50)
        print("Main Menu")
        print("=" * 50)
        print("1. Swipe on titles")
        print("2. View recommendations")
        print("3. Settings (genre preferences)")
        print("4. Exit")
        print()
        
        choice = input("Choose an option: ").strip()
        return choice
