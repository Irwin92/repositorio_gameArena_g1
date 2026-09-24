from django.db import models

class Jugador(models.Model): 
    nickname = models.CharField(max_length=60,unique=True)
    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    pais = models.CharField(max_length=80)
    nivel = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

