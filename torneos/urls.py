from django.urls import path
from . import views

urlpatterns= [
    path('',views.torneos_api, name='torneos_api'),
    path('<int:id>/',views.torneo_detalle_api, name='torneo_detalle_api'),
    path('<int:id>/inscripciones/',views.inscripciones_torneo_api,
          name='inscripciones_torneo_api'),
]