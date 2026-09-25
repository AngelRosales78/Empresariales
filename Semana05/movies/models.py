from django.db import models


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


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name='Movie',
        related_name='ratings'
    )
    reviewer = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        verbose_name='Reviewer',
        null=True,
        blank=True,
        related_name='ratings_given'
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
