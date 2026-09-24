from django.urls import path
from . import views

urlpatterns= [
    path('',views.jugadores_api, name='jugadores_api'),
    path('perfil/',views.perfil_api, name='perfil_api'),
    path('<int:id>/',views.jugador_detalle_api, name='jugador_detalle_api'),
]