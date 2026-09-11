"""
DIAGRAMA DE MODELOS DEL PROYECTO LIBRARY
========================================

Este archivo describe el diagrama ER de los modelos del proyecto.

MODELOS Y RELACIONES:
=====================

+----------------+       +------------------+       +----------------+
|    Author      |       |   AuthorProfile  |       |     Book       |
+----------------+       +------------------+       +----------------+
| id (PK)        |1    1| id (PK)          |1    1| id (PK)        |
| first_name     |------| author (FK->Auth)|------| title          |
| last_name      |  One-| phone_number     |  One-| isbn (unique)  |
| date_of_birth  |  to  | email            |  to  | publication_   |
| biography      |  One | website          |  One-| cover_image    |
+----------------+  to  | portrait (Image) |       | author_id (FK) |
     |1                +------------------+       +----------------+
     |                                             |
     | CASCADE                                     | CASCADE
     |                                             |
     v                                             v
+----------------+       +------------------+       +----------------+
|     Book       |       |    Publication   |       |   Publisher    |
| (continua)     |M    1| id (PK)          |1    1| id (PK)        |
|                |------>| book_id (FK->Book)|------| name (unique)  |
+--------+-------+       | publisher_id(FK) |       | address        |
         |               | publication_date |       | website        |
         | M          1  | edition          |       +----------------+
         |               +------------------+
         |
         v
+----------------+
|    Category    |
+----------------+
| id (PK)        |
| name (unique)  |
| description    |
+----------------+

RELACIONES:
===========

1. Book.author --> Author: ForeignKey(on_delete=CASCADE, related_name='books')
   - Un autor puede tener muchos libros
   - Al borrar autor, se borran sus libros

2. Author.profile --> AuthorProfile: OneToOneField
   - Cada autor tiene un perfil (o ninguno)
   - Datos biograficos separados del registro principal

3. Book.categories <---> Category: ManyToManyField (intermedia implicita: library_book_categories)
   - Un libro puede estar en muchas categorias
   - Una categoria puede tener muchos libros

4. Book.publications --> Publication: ManyToMany con modelo intermedio
   - Publication.linka Book con Publisher con datos extra
   - Campos extra: publication_date, edition
   - Unique together: (book, publisher)

TABLAS CREADAS:
===============

library_author                    - Autores
library_authorprofile             - Perfiles de autor (OneToOne)
library_category                  - Categorias
library_publisher                 - Editoriales
library_book                      - Libros
library_publication               - Modelo intermedio Libro-Editorial
library_book_categories           - Tabla intermedia M2M Libro-Categoria

CONSULTAS DEMOSTRATIVAS:
========================

1. book.author                     -> Forward: Libro -> Autor
2. author.books.all()              -> Reverse: Autor -> Libros
3. Book.objects.filter(author__last_name='Orwell')  -> Double underscore
4. Book.objects.filter(books__categories__name='Fiction') -> M2M filter
5. book.publications.all()         -> Through Publication
6. book.author.profile.email       -> OneToOne access
"""

print(__doc__)
