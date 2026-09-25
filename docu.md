# Django Session Exercise - Deliverable Documentation

## 1. Models

### 1.1 Genre Model
**File**: `movies/models.py` (líneas 4-16)

```python
class Genre(models.Model):
    name = models.CharField('Genre', max_length=50, unique=True)
    description = models.TextField('Description', blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name
```

**Justification de campos**:
| Campo | Tipo | Justificación |
|-------|------|---------------|
| name | CharField(max_length=50, unique=True) | El nombre del género es corto y debe ser único para evitar duplicados (ej. "Action" no puede existir dos veces). |
| description | TextField(blank=True) | Permite descripciones largas del género. `blank=True` porque es opcional. |
| created_at | DateTimeField(auto_now_add=True) | Registra automáticamente cuándo se creó el registro. |
| updated_at | DateTimeField(auto_now=True) | Se actualiza automáticamente cada vez que se modifica el registro. |

**Justificación Meta class**:
- `verbose_name` y `verbose_name_plural`: Mejor legibilidad en el Admin de Django.
- `ordering`: Ordena los géneros alfabéticamente de forma predeterminada.

---

### 1.2 Person Model
**File**: `movies/models.py` (líneas 19-32)

```python
class Person(models.Model):
    name = models.CharField('Name', max_length=100)
    nationality = models.CharField('Nationality', max_length=50, blank=True)
    birth_date = models.DateField('Birth date', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name']

    def __str__(self):
        return self.name
```

**Justificación de campos**:
| Campo | Tipo | Justificación |
|-------|------|---------------|
| name | CharField(max_length=100) | Los nombres suelen ser cortos. 100 caracteres es suficiente. |
| nationality | CharField(max_length=50, blank=True) | País de origen, opcional. |
| birth_date | DateField(null=True, blank=True) | Fecha de nacimiento, opcional y puede ser nula. |
| created_at / updated_at | DateTimeField(auto_now_add/auto_now) | Auditoría básica de registros. |

---

### 1.3 Movie Model
**File**: `movies/models.py` (líneas 35-51)

```python
class Movie(models.Model):
    title = models.CharField('Title', max_length=200)
    synopsis = models.TextField('Synopsis', blank=True)
    release_date = models.DateField('Release date', null=True, blank=True)
    duration = models.PositiveIntegerField('Duration (minutes)', null=True, blank=True)
    poster = models.ImageField('Poster', upload_to='movies/posters/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, verbose_name='Genres', blank=True, related_name='movies')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-release_date', 'title']

    def __str__(self):
        return self.title
```

**Justificación de campos**:
| Campo | Tipo | Justificación |
|-------|------|---------------|
| title | CharField(max_length=200) | Los títulos de películas pueden ser largos. |
| synopsis | TextField(blank=True) | Permite sinopsis largas. Opcional. |
| release_date | DateField(null=True, blank=True) | Fecha de lanzamiento, opcional. |
| duration | PositiveIntegerField(null=True, blank=True) | Duración en minutos (entero positivo). Opcional. |
| poster | ImageField(upload_to='movies/posters/', null=True, blank=True) | Imagen del póster. Requiere Pillow (agregado a requirements.txt). |
| genres | ManyToManyField(Genre, blank=True, related_name='movies') | Una película puede tener múltiples géneros y un género múltiples películas. `related_name='movies'` permite acceder via `genre.movies.all()`. |
| created_at / updated_at | DateTimeField(auto_now_add/auto_now) | Auditoría básica. |

**Justificación ManyToManyField**:
La relación entre película y género es claramente Many-to-Many:
- Una película puede tener varios géneros (ej. "Sci-Fi" y "Action").
- Un género puede tener muchas películas (ej. "Sci-Fi" incluye "Inception", "Interstellar", "Dune").
- Se usa `blank=True` porque al crear una película no es obligatorio asignarle un género inmediatamente.

---

### 1.4 Rating Model
**File**: `movies/models.py` (líneas 54-84)

```python
class Rating(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='Movie', related_name='ratings'
    )
    reviewer = models.ForeignKey(
        Person, on_delete=models.SET_NULL, verbose_name='Reviewer',
        null=True, blank=True, related_name='ratings_given'
    )
    score = models.PositiveSmallIntegerField('Score (1-10)')
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-score']
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=10),
                name='score_between_1_and_10'
            )
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.score}/10"
```

**Justificación de campos**:
| Campo | Tipo | Justificación |
|-------|------|---------------|
| movie | ForeignKey(Movie, on_delete=CASCADE) | Cada valoración pertenece a una sola película. CASCADE elimina valoraciones si se elimina la película. |
| reviewer | ForeignKey(Person, on_delete=SET_NULL, null=True, blank=True) | La valoración puede tener un revisor opcional. SET_NULL mantiene la valoración si se elimina al revisor. |
| score | PositiveSmallIntegerField | Puntuaciones del 1 al 10 caben en un entero pequeño positivo. |
| created_at | DateTimeField(auto_now_add=True) | Fecha de creación automática. |

**Justificación de constraint**:
```python
constraints = [
    models.CheckConstraint(
        check=models.Q(score__gte=1) & models.Q(score__lte=10),
        name='score_between_1_and_10'
    )
]
```
- El constraint se aplica **a nivel de base de datos**, no solo a nivel de formulario.
- Esto previene que se inserten valores fuera del rango 1-10 incluso si se omiten las validaciones del formulario.
- Es una capa extra de integridad de datos que no podría lograrse solo con validación de Django.

**Justificación on_delete**:
| Modelo relacionado | on_delete | Justificación |
|-------------------|-----------|---------------|
| Movie | CASCADE | Si se elimina una película, sus valoraciones también deben eliminarse (no tienen sentido sin la película). |
| Person | SET_NULL | Si se elimina un revisor, la valoración debe conservarse pero con `reviewer=NULL` (la puntuación sigue siendo válida aunque no sepamos quién la dio). |

---

## 2. Admin Configuration

**File**: `movies/admin.py` (líneas 1-41)

```python
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
```

### 2.1 Justificaciones de configuraciones de Admin

**RatingInline** (líneas 5-8):
- `model = Rating`: Permite agregar/ver valoraciones directamente desde la ficha de la película.
- `extra = 1`: Muestra un formulario vacío para agregar una valoración rápidamente.
- `raw_id_fields = ['reviewer']`: Muestra un campo de búsqueda simple en lugar de un dropdown, mejorando el rendimiento si hay muchos revisores.

**readonly_fields** en todos los ModelAdmin:
- Se marcan `created_at` y `updated_at` como de solo lectura (`readonly_fields`) porque se generan automáticamente vía `auto_now_add=True` y `auto_now=True`. Esto evita que un administrador pueda modificarlas accidentalmente, pero aún pueden verse en el formulario.

**list_filter**:
- Se usan filtros para permitir buscar rápidamente por campos como `release_date`, `genres`, `nationality`, `score`, etc.
- `list_filter = ['release_date', 'genres']` en MovieAdmin permite filtrar por rangos de fechas y por género directamente desde la lista.

**search_fields**:
- Permite búsqueda textual en campos como `title`, `synopsis`, `name`, etc.

---

## 3. Test Data Loading

**File**: `movies/management/commands/loadtest.py`

La carga de datos de prueba se realiza mediante un comando personalizado de Django:

```bash
python manage.py loadtest
```

**Datos cargados**:
| Entidad | Cantidad | Descripción |
|---------|----------|-------------|
| Genres | 4 | Sci-Fi, Drama, Action, Comedy |
| People | 6 | Directores (Nolan, Tarantino, Villeneuve, Scorsese) + Revisores (Ana García, Carlos López) |
| Movies | 10 | Inception, Interstellar, The Dark Knight, Pulp Fiction, Dune, Parasite, Mad Max: Fury Road, The Grand Budapest Hotel, The Matrix, Superbad |
| Ratings | 15 | Puntuaciones de 7-10 distribuidas entre las películas |

**Distribución de valoraciones**:
| Película | Cantidad de ratings | Puntuaciones |
|----------|--------------------|--------------|
| Inception | 3 | 9, 10, 8 (avg: 9.0) |
| Interstellar | 3 | 10, 9, 8 (avg: 9.0) |
| The Dark Knight | 3 | 10, 10, 9 (avg: 9.67) |
| Pulp Fiction | 2 | 9, 8 |
| Dune | 2 | 8, 9 |
| The Grand Budapest Hotel | 2 | 7, 8 |
| Parasite, Mad Max, The Matrix, Superbad | 0 | Sin ratings |

---

## 4. Permissions & Groups

### 4.1 Group: "editores"
**Comando ejecutado**:
```bash
python manage.py shell -c "
from django.contrib.auth.models import Group, Permission
from movies.models import Movie
group, _ = Group.objects.get_or_create(name='editores')
perms = ['add_movie', 'change_movie']
for codename in perms:
    perm = Permission.objects.get(codename=codename, content_type__app_label='movies', content_type__model='movie')
    group.permissions.add(perm)
"
```

### 4.2 User: "editor_prueba"
**Comando ejecutado**:
```bash
python manage.py shell -c "
from django.contrib.auth.models import User, Group
user, _ = User.objects.get_or_create(username='editor_prueba')
user.set_password('Editor@12345')
user.is_staff = True
user.is_superuser = False
user.save()
group = Group.objects.get(name='editores')
user.groups.add(group)
"
```

**Permisos asignados**:
| Permiso | Descripción |
|---------|-------------|
| movies.add_movie | Puede agregar nuevas películas |
| movies.change_movie | Puede editar películas existentes |

**Permisos NO asignados**:
| Permiso | Consecuencia |
|---------|-------------|
| movies.delete_movie | No puede eliminar películas |
| movies.add_genre, change_genre, delete_genre | No puede gestionar géneros |
| movies.add_person, change_person, delete_person | No puede gestionar personas |
| movies.add_rating, change_rating, delete_rating | No puede gestionar valoraciones |

**Resultado**: El usuario `editor_prueba` con contraseña `Editor@12345` puede acceder al Admin de Django y solo verá y modificará películas (agregar y editar), pero no podrá ver ni modificar géneros, personas ni valoraciones.

---

## 5. Public Views

### 5.1 View: index
**File**: `movies/views.py` (líneas 36-46)

```python
def index(request):
    movies = Movie.objects.annotate(
        avg_score=Avg('ratings__score'),
        num_ratings=Count('ratings__score')
    ).order_by('-release_date')
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)
```

**Justificación**:
- `annotate(avg_score=Avg('ratings__score'))`: Calcula la puntuación media de cada película usando Django ORM. Esto es más eficiente que calcularlo en Python porque se realiza a nivel de base de datos.
- `annotate(num_ratings=Count('ratings__score'))`: Cuenta cuántas valoraciones tiene cada película.
- `order_by('-release_date')`: Las películas más recientes se muestran primero.
- Los annotates se calculan una sola vez para todas las películas, evitando el problema N+1 de queries.

### 5.2 View: movie_recommendations
**File**: `movies/views.py` (líneas 6-33)

```python
def movie_recommendations(request, movie_id):
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
```

**Justificación**:
- `filter(genres__in=genres)`: Encuentra películas que comparten al menos un género con la película actual.
- `exclude(pk=movie_id)`: Excluye la película actual de los resultados.
- `filter(num_ratings__gte=1)`: Solo muestra películas que tienen al menos 1 valoración (evita mostrar películas sin ratings).
- `order_by('-avg_score')`: Ordena por puntuación media más alta.
- `distinct()`: Elimina duplicados causados por la combinación de ManyToMany con annotation.

---

## 6. URLs Configuration

### 6.1 Root URLs - `config/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('library/', include('library.urls')),
]
```
- **Justificación**: `movies/` se incluye en las URLs raíz para que las vistas públicas sean accesibles desde `/movies/`.

### 6.2 App URLs - `movies/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/<int:movie_id>/', views.movie_recommendations, name='recommendations'),
]
```
- **Justificación**: 
  - `/movies/` -> Muestra todas las películas con sus puntuaciones.
  - `/movies/recommendations/<id>/` -> Muestra recomendaciones para una película específica.

---

## 7. Templates

### 7.1 Base Template - `templates/movies/base.html`
- Diseño oscuro con tema de cine (#1a1a2e, #e94560).
- Incluye navegación: "All Movies" y "Admin Panel".
- Define bloques: `{% block title %}` y `{% block content %}`.

### 7.2 Index Template - `templates/movies/index.html`
- Tabla con columnas: Title, Release Date, Avg Score, Ratings, Recommendations.
- Cada título es enlace a la página de recomendaciones.

### 7.3 Recommendations Template - `templates/movies/recommendations.html`
- Muestra información de la película seleccionada (título, géneros, duración, rating promedio).
- Lista películas recomendadas del mismo género ordenadas por puntuación.

---

## 8. Migration

**File**: `movies/migrations/0001_initial.py`

La migración crea 4 tablas:
1. `movies_genre` - Con campos: id, name (unique), description, created_at, updated_at
2. `movies_person` - Con campos: id, name, nationality, birth_date, created_at, updated_at
3. `movies_movie` - Con campos: id, title, synopsis, release_date, duration, poster, created_at, updated_at
4. `movies_movie_genres` - Tabla intermedia para ManyToManyField entre Movie y Genre
5. `movies_rating` - Con campos: id, movie_id (FK), reviewer_id (FK), score, created_at
   - Constraint: `score_between_1_and_10` (score >= 1 AND score <= 10)

---

## 9. Requirements

**File**: `requirements.txt`
```
Django==5.2.17
Pillow==12.0.0
```

- **Django**: Framework principal.
- **Pillow**: Biblioteca de procesamiento de imágenes requerida por `models.ImageField` para los pósteres de películas.

---

## 10. Test Cases

### Test Case 1: Admin Access - Superuser
**Usuario**: `admin` / `Admin@12345`
**Acción**: Ingresar a `/admin/`
**Resultado esperado**: Acceso completo a todos los modelos (Genre, Person, Movie, Rating) con todas las operaciones (add, change, delete).

### Test Case 2: Admin Access - Editor
**Usuario**: `editor_prueba` / `Editor@12345`
**Acción**: Ingresar a `/admin/`
**Resultado esperado**: Solo puede ver y gestionar Movies (add, change). No puede ver ni modificar Genres, Persons, ni Ratings.

### Test Case 3: Public Movies Listing
**URL**: `/movies/`
**Acción**: Navegar a la página principal de películas
**Resultado esperado**: Se muestran las 10 películas con sus títulos, fecha de lanzamiento, puntuación promedio y cantidad de ratings. Las películas con ratings muestran valores numéricos; las sin ratings muestran "N/A".

### Test Case 4: Movie Recommendations
**URL**: `/movies/recommendations/1/` (Inception)
**Acción**: Hacer clic en "Recommendations" para Inception
**Resultado esperado**: Se muestra:
- Info de Inception con avg_score de 9.0/10
- Lista de recomendaciones del mismo género (Sci-Fi) ordenadas por puntuación: The Dark Knight (si tiene genres cruzados), Interstellar, Dune, The Matrix

### Test Case 5: Rating Constraint
**Acción**: Intentar crear una Rating con score=0 o score=11 vía Admin o API
**Resultado esperado**: Django rechazará el valor con error de validación "Ensure this value is less than or equal to 10" o "Ensure this value is greater than or equal to 1".

### Test Case 6: Data Integrity via loadtest
**Comando**: `python manage.py loadtest`
**Resultado esperado**: 
```
  Genre created: Sci-Fi
  Genre created: Drama
  Genre created: Action
  Genre created: Comedy
  Person created: Christopher Nolan
  Person created: Quentin Tarantino
  Person created: Denis Villeneuve
  Person created: Martin Scorsese
  Person created: Ana García
  Person created: Carlos López
  Movie created: Inception
  Movie created: Interstellar
  ... (8 más)
  Rating created: Inception - 9/10
  ... (14 más)
Data loaded: 4 genres, 6 people, 10 movies, 15 ratings
```

### Test Case 7: Idempotency of loadtest
**Comando**: Ejecutar `python manage.py loadtest` dos veces consecutivas
**Resultado esperado**: El segundo ejecución no duplica datos porque usa `get_or_create()`. Muestra "Data loaded: 4 genres, 6 people, 10 movies, 15 ratings" sin crear entidades duplicadas.

---

## 11. Screenshot Descriptions

### Screenshot 1: Admin - All Models
**URL**: `http://127.0.0.1:8000/admin/`
**Descripción**: Panel de Admin mostrando las 4 aplicaciones: Genre, Person, Movie, Rating. Cada uno con contador de instancias.

### Screenshot 2: Admin - Movie Detail with Inline Ratings
**URL**: `http://127.0.0.1:8000/admin/movies/movie/1/change/`
**Descripción**: Ficha de "Inception" mostrando campos editables (title, synopsis, release_date, duration, genres, poster) y campos readonly (created_at, updated_at). Inline de Ratings mostrando valoraciones asociadas.

### Screenshot 3: Admin - Editor Permissions
**URL**: `http://127.0.0.1:8000/admin/` (login como editor_prueba)
**Descripción**: Panel de Admin mostrando solo "Movies" como opción disponible. No se ven Genre, Person, ni Rating.

### Screenshot 4: Public - Movies Listing
**URL**: `http://127.0.0.1:8000/movies/`
**Descripción**: Página principal mostrando tabla con 10 películas, sus puntuaciones promedio y enlaces a recomendaciones.

### Screenshot 5: Public - Movie Recommendations
**URL**: `http://127.0.0.1:8000/movies/recommendations/2/` (The Dark Knight)
**Descripción**: Página mostrando info de The Dark Knight (Drama, Action) y lista de recomendaciones ordenadas por puntuación media.

---

## 12. Project Structure

```
C:\Users\ADMIN\Documents\Default Project\
├── config/
│   ├── __init__.py
│   ├── settings.py          # INSTALLED_APPS includes 'movies'
│   ├── urls.py              # Includes 'movies/urls'
│   └── wsgi.py
├── library_project/
│   └── settings.py          # Alias/backup
├── movies/
│   ├── __init__.py
│   ├── admin.py             # ModelAdmin + Inlines
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py  # Creates Genre, Person, Movie, Rating tables
│   ├── models.py            # Genre, Person, Movie, Rating
│   ├── urls.py              # index + recommendations routes
│   └── views.py             # index + movie_recommendations views
│   └── management/commands/loadtest.py  # Data loading command
├── templates/
│   └── movies/
│       ├── base.html         # Dark theme base template
│       ├── index.html        # Movies listing table
│       └── recommendations.html  # Recommendation details
├── templates/
│   └── library/
│       ├── base.html
│       ├── index.html
│       ├── book_form.html
│       └── detail.html
├── db.sqlite3               # Database with test data
├── manage.py
├── requirements.txt         # Django==5.2.17, Pillow==12.0.0
└── docu.md                  # This file
```

---

## 13. Key Design Decisions Summary

| Decision | Alternative Considered | Rationale |
|----------|----------------------|-----------|
| ManyToManyField para Movie-Genre | ForeignKey en Movie o tabla intermedia manual | M2M es la relación natural. Django la maneja automáticamente con una tabla intermedia. |
| PositiveSmallIntegerField para score | IntegerField con validación de formulario | Constraint a nivel DB previene datos inválidos incluso bypass de Django. |
| ImageField con Pillow | CharField para URL de imagen | Pillow es estándar en el ecosistema Django para ImageField. |
| TabularInline para Ratings | StackbarInline | Tabular es más compacto y apropiado para campos simples de rating. |
| SET_NULL para reviewer | CASCADE o SET_DEFAULT | SET_NULL conserva la valoración aunque el revisor se elimine. |
| readonly_fields para timestamps | No mostrar en admin | Los timestamps se generan automáticamente; readonly permite verlos pero no editarlos. |
| annotate() en views | Query en Python con loop | Annotate es eficiente (SQL-level), evita N+1 queries. |
| CheckConstraint en model | Validación solo en form/serializer | Constraint DB es la capa final de protección para integridad de datos. |
