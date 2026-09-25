from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from .models import Movie, Genre


def movie_recommendations(request, movie_id):
    """
    Muestra recomendaciones de películas: del mismo género que la película
    seleccionada, ordenadas por puntuación media más alta (con al menos 1 valoración).
    """
    current_movie = get_object_or_404(Movie, pk=movie_id)
    genres = current_movie.genres.all()

    recommendations = (
        Movie.objects
        .filter(genres__in=genres)
        .exclude(pk=movie_id)
        .annotate(
            avg_score=Avg('ratings__score'),
            num_ratings=Count('ratings__score')
        )
        .filter(num_ratings__gte=1)
        .order_by('-avg_score')
        .distinct()
    )

    context = {
        'current_movie': current_movie,
        'recommendations': recommendations,
        'current_avg': current_movie.ratings.aggregate(Avg('score'))['score__avg'],
        'current_num_ratings': current_movie.ratings.count(),
    }
    return render(request, 'movies/recommendations.html', context)


def index(request):
    """Página principal con listado de todas las películas."""
    movies = Movie.objects.annotate(
        avg_score=Avg('ratings__score'),
        num_ratings=Count('ratings__score')
    ).order_by('-release_date')

    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)
