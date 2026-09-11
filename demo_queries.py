import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library.models import Author, AuthorProfile, Book, Category, Publisher, Publication


def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


# ==================== STEP 9: QUERY DEMONSTRATION ====================

print_section("STEP 9 - CONSOLE QUERIES DEMONSTRATION")

# --- Query 1: Forward (book -> author) ---
print_section("Query 1: Forward Query - Book.author (book -> author)")
book = Book.objects.get(title="1984")
print(f"Book: {book.title}")
print(f"Book.author (forward FK): {book.author}")
print(f"Author first_name: {book.author.first_name}")
print(f"Author last_name: {book.author.last_name}")
print(f"Author date_of_birth: {book.author.date_of_birth}")
print(f"Author biography: {book.author.biography}")

# --- Query 2: Reverse (author -> books) ---
print_section("Query 2: Reverse Query - Author.books.all() (author <- books)")
author = Author.objects.get(first_name="Gabriel", last_name="García Márquez")
print(f"Author: {author}")
print(f"Author.books.all() (reverse FK):")
for b in author.books.all():
    print(f"  - {b.title} (ISBN: {b.isbn})")

# --- Query 3: Double underscore filtering ---
print_section("Query 3: Filter with Double Underscore - author__last_name")
print("Books by authors with last_name='Orwell':")
books = Book.objects.filter(author__last_name="Orwell")
for b in books:
    print(f"  - {b.title}")

print("\nAuthors who wrote books in 'Fiction' category:")
authors = Author.objects.filter(books__categories__name="Fiction").distinct()
for a in authors:
    print(f"  - {a.first_name} {a.last_name}")

print("\nBooks published by 'Penguin Books':")
books = Book.objects.filter(publications__publisher__name="Penguin Books")
for b in books:
    print(f"  - {b.title} ({b.publications.filter(publisher__name='Penguin Books').first().edition})")

# --- Query 4: Through Publication ---
print_section("Query 4: Through Publication - Book -> Publisher via intermediate")
book = Book.objects.get(title="1984")
print(f"Book: {book.title}")
print(f"Publications (Publisher + Edition):")
for pub in book.publications.all():
    print(f"  - Publisher: {pub.publisher}, Edition: {pub.edition}, Date: {pub.publication_date}")

# --- Query 5: Many-to-Many ---
print_section("Query 5: Many-to-Many - Book.categories.all()")
book = Book.objects.get(title="1984")
print(f"Book: {book.title}")
print(f"Categories:")
for cat in book.categories.all():
    print(f"  - {cat.name}: {cat.description}")

# --- Query 6: Author Profile ---
print_section("Query 6: OneToOne - Author.profile")
author = Author.objects.get(first_name="George", last_name="Orwell")
print(f"Author: {author}")
print(f"Profile email: {author.profile.email}")
print(f"Profile phone: {author.profile.phone_number}")
print(f"Profile website: {author.profile.website}")

# --- Query 7: Filtering through Publication ---
print_section("Query 7: Filter Book through Publication.publication_date__year")
print("Books published by Penguin Books after 1960:")
books = Book.objects.filter(
    publications__publisher__name="Penguin Books",
    publications__publication_date__year__gte=1960
).distinct()
for b in books:
    pubs = b.publications.filter(publisher__name="Penguin Books", publication_date__year__gte=1960)
    for pub in pubs:
        print(f"  - {b.title} ({pub.edition}, {pub.publication_date})")

print_section("QUERIES COMPLETE - All queries executed successfully")
