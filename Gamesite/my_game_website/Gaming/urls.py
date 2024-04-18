from django.urls import path
from . import views
from .views import welcome

urlpatterns = [
    path('', welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('games/', views.games, name='games'),
]