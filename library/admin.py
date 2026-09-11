from django.contrib import admin
from .models import Author, AuthorProfile, Category, Publisher, Book, Publication


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth']
    search_fields = ['first_name', 'last_name']


class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile
    can_delete = False


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'publication_date']
    filter_horizontal = ['categories']
    search_fields = ['title', 'isbn']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
