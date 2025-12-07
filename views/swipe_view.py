# display swipe interface

class SwipeView:
    def show_title(self, title):
        year_val = title.release_year if title.release_year else '?'
        print("\n" + "-" * 50)
        print(f"{title.title} ({year_val}) - {title.type}")
        print(f"rating: {title.age_rating}")
        if title.duration_value and title.duration_unit:
            print(f"duration: {title.duration_value} {title.duration_unit}")
        genres = ', '.join([g.name for g in title.genres]) if title.genres else 'unknown'
        print(f"genres: {genres}")
        print(f"description: {title.description}")
        print("-" * 50)
        print("Y = interested, N = not interested, X = exit")

    def no_titles_left(self):
        print("\nno more titles to swipe right now")

    def get_choice(self):
        while True:
            choice = input("Your choice (Y/N/X): ").strip().lower()
            if choice in ['y', 'n', 'x']:
                return choice
            print("please enter Y, N, or X")