from django.db import models
from django.conf import settings
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AuthorProfile(models.Model):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    portrait = models.ImageField(upload_to='author_portraits/', blank=True)

    class Meta:
        verbose_name = 'Author Profile'
        verbose_name_plural = 'Author Profiles'

    def __str__(self):
        return f'Profile of {self.author}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class Publication(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='publications')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='publications')
    publication_date = models.DateField(null=True, blank=True)
    edition = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['publisher', 'publication_date']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        unique_together = ('book', 'publisher')

    def __str__(self):
        return f'{self.book} - {self.publisher} ({self.edition or "N/A"})'
