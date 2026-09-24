from django.db import models

class Videojuego(models.Model): 
    nombre = models.CharField(max_length=120)
    genero = models.CharField(max_length=80)
    plataforma = models.CharField(max_length=80)
    clasificacion = models.CharField(max_length=30, blank=True)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
