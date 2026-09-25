from django.contrib import admin
from .models import Genre, Person, Movie, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    raw_id_fields = ['reviewer']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'created_at']
    list_filter = ['nationality', 'created_at']
    search_fields = ['name', 'nationality']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'duration', 'created_at']
    list_filter = ['release_date', 'genres']
    search_fields = ['title', 'synopsis']
    inlines = [RatingInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'reviewer', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['movie__title']
    readonly_fields = ['created_at']
