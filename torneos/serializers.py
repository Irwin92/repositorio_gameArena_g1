from rest_framework import serializers
from .models import Torneo,Inscripcion

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields= '__all__'
#----------------------------------------------------------------------
    def validate_cupo_maximo(self,value):
        if value<2:
            raise serializers.ValidationError(
                'El cupo maximo debe ser al menos 2.'
            )
        return value
#----------------------------------------------------------------------
    def validate(self,data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        videojuego = data.get('videojuego')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'No puede ser anterior a la fecha de inicio.'
            })

        if videojuego and not videojuego.activo:
            raise serializers.ValidationError({
                'videojuego': 'No se puede usar un videojuego inactivo.'
            })
        return data

#----------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#----------------------------------------------------------------------
class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields= '__all__'
        read_only_fields =['fecha_inscripcion']

#----------------------------------------------------------------------
    def validate(self, data):
        torneo = data.get('torneo')
        jugador = data.get('jugador')

        if not jugador.activo:
            raise serializers. ValidationError(
                'No se puede inscribir un jugador inactivo.'
            )
        if torneo.estado != 'ABIERTO':
            raise serializers.ValidationError(
                'El torneo no está abierto para inscripciones.'
            )
        if Inscripcion.objects.filter(
            torneo=torneo,
            jugador=jugador
        ).exists():
            raise serializers.ValidationError(
                'El jugador ya está inscrito en este torneo.'
            )

        participantes = torneo.inscripciones.filter(
            estado='ACTIVA'
            ).count()

        if participantes >= torneo.cupo_maximo:
            raise serializers.ValidationError(
                'El torneo alcanzó su cupo maximo.'
            )
        return data
#----------------------------------------------------------------------

#----------------------------------------------------------------------