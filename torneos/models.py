from django.db import models
from videojuegos.models import Videojuego 
from jugadores.models import Jugador


class Torneo(models.Model): 
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('EN_CURSO', 'En curso'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]
    nombre = models.CharField(max_length=120)
    videojuego = models.ForeignKey(
        Videojuego,
        on_delete=models.PROTECT,
        related_name='torneos'
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    cupo_maximo = models.PositiveIntegerField()
    estado= models.CharField(max_length=20, choices=ESTADOS,default='ABIERTO')
    premio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
            return self.nombre
#----------------------------------------------------------------------------------------------------    
class Inscripcion(models.Model): 
    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('RETIRADA', 'Retirada'),
        ('DESCALIFICADA', 'Descalificada'),
    ]
    
    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    jugador = models.ForeignKey(
            Jugador,
            on_delete=models.CASCADE,#Si elimina el objeto principal tambie todos los registros relacionados
            related_name='inscripciones'
        )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado= models.CharField(max_length=20, choices=ESTADOS,default='Activa')

    class Meta: 
         constraints=[
              models.UniqueConstraint(
                   fields=['torneo','jugador'],
                   name='inscripcion_unica_torneo_jugador'
              )
         ]
    def __str__(self):
         return f'{self.jugador} - {self.torneo}'