from rest_framework import serializers
from .models import Videojuego

class VideoJuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videojuego
        fields= '__all__'