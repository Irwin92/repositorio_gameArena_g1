from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from jugadores.models import Jugador
from videojuegos.models import VideoJuego
from .models import Torneo, Inscripcion
from .serializers import TorneoSerializer, InscripcionSerializer


def paginar_torneos(queryset, page_number):
    paginator = Paginator(queryset, 5)
    page = paginator.get_page(page_number)
    return Response({
        'pagina_actual': page.number,
        'total_paginas': paginator.num_pages,
        'total_registros': paginator.count,
        'resultados': TorneoSerializer(page.object_list, many=True).data
    })

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(['GET', 'POST'])
def torneos_api(request):
    if request.method == 'GET':
        torneos = Torneo.objects.select_related('videojuego').order_by('fecha_inicio')
        estado = request.query_params.get('estado')
        videojuego = request.query_params.get('videojuego')

        if estado:
            torneos = torneos.filter(estado=estado.upper())
        if videojuego:
            torneos = torneos.filter(videojuego_id=videojuego)

        return paginar_torneos(torneos, request.query_params.get('page', 1))

    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'detail': 'Se requiere administrador.'}, status=403)

    serializer = TorneoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def torneo_detalle_api(request, id):
    try:
        torneo = Torneo.objects.select_related('videojuego').get(id=id)
    except Torneo.DoesNotExist:
        return Response({'error': 'Torneo no encontrado.'}, status=404)

    if request.method == 'GET':
        return Response(TorneoSerializer(torneo).data)

    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'detail': 'Se requiere administrador.'}, status=403)

    if request.method in ['PUT', 'PATCH']:
        serializer = TorneoSerializer(
            torneo, data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    torneo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            #endPoints de inscripciones
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(['GET', 'POST'])
def inscripciones_torneo_api(request, id):
    try:
        torneo = Torneo.objects.get(id=id)
    except Torneo.DoesNotExist:
        return Response({'error': 'Torneo no encontrado.'}, status=404)

    if request.method == 'GET':
        inscripciones = torneo.inscripciones.select_related('jugador').order_by(
            'fecha_inscripcion'
        )
        return Response(
            InscripcionSerializer(inscripciones, many=True).data,
            status=status.HTTP_200_OK
        )

    if not request.user.is_authenticated:
        return Response(
            {'detail': 'Debe autenticarse para registrar una inscripción.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    data = request.data.copy()
    data['torneo'] = torneo.id
    serializer = InscripcionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def estadisticas_admin_api(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Autenticación requerida.'}, status=401)
    if not request.user.is_staff:
        return Response({'detail': 'Se requiere administrador.'}, status=403)

    mayor = Torneo.objects.annotate(
        participantes=Count(
            'inscripciones',
            filter=Q(inscripciones__estado='ACTIVA')
        )
    ).order_by('-participantes', 'nombre').first()

    torneo_mayor = None
    if mayor:
        torneo_mayor = {
            'id': mayor.id,
            'nombre': mayor.nombre,
            'participantes': mayor.participantes
        }

    return Response({
        'videojuegos_activos': Videojuego.objects.filter(activo=True).count(),
        'jugadores_activos': Jugador.objects.filter(activo=True).count(),
        'torneos_abiertos': Torneo.objects.filter(estado='ABIERTO').count(),
        'inscripciones_activas': Inscripcion.objects.filter(
            estado='ACTIVA'
        ).count(),
        'torneo_mayor_participacion': torneo_mayor
    })


