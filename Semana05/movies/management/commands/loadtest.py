from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from movies.models import Genre, Person, Movie, Rating


class Command(BaseCommand):
    help = 'Load test data for the movies app'

    def handle(self, *args, **kwargs):
        # --- Géneros ---
        genres_data = [
            {'name': 'Sci-Fi', 'description': 'Ciencia ficción'},
            {'name': 'Drama', 'description': 'Drama'},
            {'name': 'Action', 'description': 'Acción'},
            {'name': 'Comedy', 'description': 'Comedia'},
        ]
        genres = []
        for g in genres_data:
            genre, created = Genre.objects.get_or_create(name=g['name'], defaults={'description': g['description']})
            genres.append(genre)
            if created:
                self.stdout.write(f'  Genre created: {genre.name}')

        # --- Personas (directores y revisores) ---
        people_data = [
            {'name': 'Christopher Nolan', 'nationality': 'British', 'birth_date': date(1970, 7, 30)},
            {'name': 'Quentin Tarantino', 'nationality': 'American', 'birth_date': date(1963, 3, 27)},
            {'name': 'Denis Villeneuve', 'nationality': 'Canadian', 'birth_date': date(1967, 10, 3)},
            {'name': 'Martin Scorsese', 'nationality': 'American', 'birth_date': date(1942, 11, 17)},
            {'name': 'Ana García', 'nationality': 'Spanish', 'birth_date': date(1985, 5, 12)},
            {'name': 'Carlos López', 'nationality': 'Mexican', 'birth_date': date(1990, 8, 20)},
        ]
        people = []
        for p in people_data:
            person, created = Person.objects.get_or_create(
                name=p['name'],
                defaults={'nationality': p['nationality'], 'birth_date': p['birth_date']}
            )
            people.append(person)
            if created:
                self.stdout.write(f'  Person created: {person.name}')

        # --- Películas ---
        movies_data = [
            {
                'title': 'Inception',
                'synopsis': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_date': date(2010, 7, 16),
                'duration': 148,
                'genres': [genres[0]],  # Sci-Fi
            },
            {
                'title': 'Interstellar',
                'synopsis': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'release_date': date(2014, 11, 7),
                'duration': 169,
                'genres': [genres[0]],  # Sci-Fi
            },
            {
                'title': 'The Dark Knight',
                'synopsis': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest tests.',
                'release_date': date(2008, 7, 18),
                'duration': 152,
                'genres': [genres[2], genres[1]],  # Action, Drama
            },
            {
                'title': 'Pulp Fiction',
                'synopsis': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
                'release_date': date(1994, 10, 14),
                'duration': 154,
                'genres': [genres[1], genres[2]],  # Drama, Action
            },
            {
                'title': 'Dune',
                'synopsis': 'A noble family becomes embroiled in a war for control over the galaxy\'s most valuable asset.',
                'release_date': date(2021, 10, 22),
                'duration': 155,
                'genres': [genres[0]],  # Sci-Fi
            },
            {
                'title': 'Parasite',
                'synopsis': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                'release_date': date(2019, 5, 30),
                'duration': 132,
                'genres': [genres[1]],  # Drama
            },
            {
                'title': 'Mad Max: Fury Road',
                'synopsis': 'In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland.',
                'release_date': date(2015, 5, 15),
                'duration': 120,
                'genres': [genres[2]],  # Action
            },
            {
                'title': 'The Grand Budapest Hotel',
                'synopsis': 'A writer encounters the owner of an aging high-class hotel, who tells of his early years as a lobby boy.',
                'release_date': date(2014, 3, 28),
                'duration': 99,
                'genres': [genres[3]],  # Comedy
            },
            {
                'title': 'The Matrix',
                'synopsis': 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth.',
                'release_date': date(1999, 3, 31),
                'duration': 136,
                'genres': [genres[0], genres[2]],  # Sci-Fi, Action
            },
            {
                'title': 'Superbad',
                'synopsis': 'Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party.',
                'release_date': date(2007, 8, 17),
                'duration': 113,
                'genres': [genres[3]],  # Comedy
            },
        ]

        movies = []
        for m in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=m['title'],
                defaults={
                    'synopsis': m['synopsis'],
                    'release_date': m['release_date'],
                    'duration': m['duration'],
                }
            )
            if created:
                self.stdout.write(f'  Movie created: {movie.title}')
            movie.genres.set(m['genres'])
            movies.append(movie)

        # --- Valoraciones ---
        ratings_data = [
            # Inception (5 ratings)
            {'movie': movies[0], 'reviewer': people[4], 'score': 9},
            {'movie': movies[0], 'reviewer': people[5], 'score': 10},
            {'movie': movies[0], 'reviewer': people[0], 'score': 8},
            # Interstellar (3 ratings)
            {'movie': movies[1], 'reviewer': people[4], 'score': 10},
            {'movie': movies[1], 'reviewer': people[5], 'score': 9},
            {'movie': movies[1], 'reviewer': people[1], 'score': 8},
            # The Dark Knight (4 ratings)
            {'movie': movies[2], 'reviewer': people[4], 'score': 10},
            {'movie': movies[2], 'reviewer': people[5], 'score': 10},
            {'movie': movies[2], 'reviewer': people[0], 'score': 9},
            # Pulp Fiction (2 ratings)
            {'movie': movies[3], 'reviewer': people[1], 'score': 9},
            {'movie': movies[3], 'reviewer': people[2], 'score': 8},
            # Dune (3 ratings)
            {'movie': movies[4], 'reviewer': people[4], 'score': 8},
            {'movie': movies[4], 'reviewer': people[2], 'score': 9},
            # The Grand Budapest Hotel (2 ratings)
            {'movie': movies[7], 'reviewer': people[4], 'score': 7},
            {'movie': movies[7], 'reviewer': people[5], 'score': 8},
        ]

        for r in ratings_data:
            rating, created = Rating.objects.get_or_create(
                movie=r['movie'],
                reviewer=r['reviewer'],
                score=r['score']
            )
            if created:
                self.stdout.write(f'  Rating created: {rating.movie.title} - {rating.score}/10')

        self.stdout.write(self.style.SUCCESS(f'\nData loaded: {len(genres)} genres, {len(people)} people, {len(movies)} movies, {len(ratings_data)} ratings'))
