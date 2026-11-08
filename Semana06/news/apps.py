from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    label = 'appnews'  # Conserva la identidad de las migraciones existentes.
    verbose_name = 'Noticias'
