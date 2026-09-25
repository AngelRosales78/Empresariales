from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/<int:movie_id>/', views.movie_recommendations, name='recommendations'),
]
