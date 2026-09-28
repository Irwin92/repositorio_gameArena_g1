from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import VideoJuego
from .serializers import VideoJuegoSerializer

@api_view(['GET','POST'])
def videojuegos_api(request):
    if request.method == 'GET':
        videojuegos = VideoJuego.objects.filter(activo=True).order_by('nombre')
        plataforma = request.query_params_get('plataforma')

        if plataforma:
            videojuegos =videojuegos.filter(plataforma__iexact=plataforma)

        serializer= VideoJuegoSerializer(videojuegos,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
        {'detail':'Se requiere un usuario administrador.'},
        status=status.HTTP_403_FORBIDDEN
        )

    serializer = VideoJuegoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@api_view(['GET','PUT','PATCH','DELETE'])
def videojuego_detalle_api(request, id):
    try:
        videojuego= VideoJuego.objects.get(id=id) 
    except VideoJuego.DoesNotExist:
        return Response(
            {'error':'Videojuego no enconcontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        request.session['ultimo_videojuego_id'] = videojuego.id
        request.session['ultimo_videojuego_nombre'] = videojuego.nombre
        return Response(VideoJuegoSerializer(videojuego).data)

    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'detail':'Se requiere un usuario administrador.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method in ['PUT','PATCH']:
        serializer = VideoJuegoSerializer(
            videojuego,
            data = request.data,
            partial = request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    videojuego.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@api_view(['GET'])
def ultimo_videojuego_api(request):
     return Response({
        'id':request.session.get('ultimo_videojuego_id'),
        'nombre':request.session.get('ultimo_videojuego_nombre')
        })