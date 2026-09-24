from django.urls import path
from . import views

urlpatterns= [
    path('',views.videojuegos_api, name='videojuegos_api'),
    path('ultimo-visitado/',views.ultimo_videojuego_api, name='ultimo_videojuego_api'),
    path('<int:id>/',views.videojuego_detalle_api, name='videojuego_detalle_api'),
]