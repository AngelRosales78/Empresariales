from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', unique=True, max_length=100)
    description = models.TextField('Descripci\u00f3n', blank=True)
    created_at = models.DateTimeField('Creado el', auto_now_add=True)

    class Meta:
        verbose_name = 'Categor\u00eda'
        verbose_name_plural = 'Categor\u00edas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('appnews:category_detail', kwargs={'slug': self.slug})


class Author(models.Model):
    name = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Email', blank=True)
    bio = models.TextField('Biograf\u00eda', blank=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('Creado el', auto_now_add=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('appnews:home')


class Article(models.Model):
    title = models.CharField('T\u00edtulo', max_length=200)
    slug = models.SlugField('Slug', unique=True, max_length=200)
    summary = models.TextField('Resumen', blank=True)
    content = models.TextField('Contenido')
    featured_image = models.ImageField('Imagen destacada', upload_to='articles/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles', verbose_name='Autor')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='Categor\u00eda')
    categories = models.ManyToManyField(Category, blank=True, related_name='articles_multi', verbose_name='Categor\u00edas')
    published_at = models.DateTimeField('Fecha de publicaci\u00f3n', auto_now_add=True)
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Art\u00edculo'
        verbose_name_plural = 'Art\u00edculos'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('appnews:article_detail', kwargs={'slug': self.slug})

    @property
    def main_category(self):
        return self.category
