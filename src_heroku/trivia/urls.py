from django.urls import path
from . import views

app_name = 'trivia'

urlpatterns = [
    path('tablero_puntuacion/', views.tablero_puntuacion, name='tablero_puntuacion'),
    path('crear_pregunta/', views.crear_pregunta, name='crear_pregunta'),
    path('jugar/', views.jugar, name='jugar'),
]
