# show recommendations

class RecommendationView:
    def show_filters(self):
        print("\nfilters (leave blank to skip)")
        type_filter = input("type (Movie/TV Show): ").strip()
        year_min = input("min year: ").strip()
        year_max = input("max year: ").strip()
        rating = input("age rating (e.g. TV-MA, PG): ").strip()
        
        filters = {}
        if type_filter:
            filters['type'] = type_filter
        if year_min.isdigit():
            filters['year_min'] = int(year_min)
        if year_max.isdigit():
            filters['year_max'] = int(year_max)
        if rating:
            filters['rating'] = rating
        return filters
    
    def show_recommendations(self, recs):
        if not recs:
            print("\nno recommendations yet. try swiping more")
            return
        
        print("\nTop picks:")
        for score, title in recs:
            genres = ", ".join([g.name for g in title.genres])
            duration = f"{title.duration_value} {title.duration_unit}" if title.duration_value else ""
            print("\n" + "-" * 40)
            print(f"{title.title} ({title.type}, {title.release_year})")
            print(f"rating: {title.age_rating}   duration: {duration}")
            print(f"genres: {genres}")
            print(f"score: {score}")
            print(f"{title.description}")