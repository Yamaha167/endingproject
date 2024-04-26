from django.urls import path
from . import views
from .views import welcome, FileUploadView, SuccessView, GameDetailView


urlpatterns = [
    path('', welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('games/', views.games, name='games'),
    path('games/<slug:slug>/', GameDetailView.as_view(), name='game_detail'),
    path('flappy_game/', views.flappygame, name='flappy_game'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('success/', SuccessView.as_view(), name='file_upload_success'),
]