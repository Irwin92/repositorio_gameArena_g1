from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Jugador
from .serializers import JugadorSerializer

# El listado incorporará paginacion filtro combinado por país y estado
# y busquesa parcial por nickname
# La creacion,actualización y eliminación se reservan para administradores
def respuesta_paginada(queryset, serializer_class, page_number):
    paginator = Paginator(queryset, 5)
    page = paginator.get_page(page_number)
    serializer = serializer_class(page.object_list, many=True)
    return Response({
        'pagina_actual': page.number,
        'total_paginas': paginator.num_pages,
        'total_registros': paginator.count,
        'resultados': serializer.data
    })

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(['GET', 'POST'])
def jugadores_api(request):
    if request.method == 'GET':
        jugadores = Jugador.objects.order_by('nickname')
        pais = request.query_params.get('pais')
        activo = request.query_params.get('activo')
        buscar = request.query_params.get('buscar')

        if pais:
            jugadores = jugadores.filter(pais__iexact=pais)
        if activo is not None:
            if activo.lower() not in ['true', 'false']:
                return Response(
                    {'activo': 'Utilice true o false.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            jugadores = jugadores.filter(activo=activo.lower() == 'true')
        if buscar:
            jugadores = jugadores.filter(nickname__icontains=buscar)

        return respuesta_paginada(
            jugadores, JugadorSerializer,
            request.query_params.get('page', 1)
        )

    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'detail': 'Se requiere administrador.'}, status=403)

    serializer = JugadorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def jugador_detalle_api(request, id):
    try:
        jugador = Jugador.objects.get(id=id)
    except Jugador.DoesNotExist:
        return Response({'error': 'Jugador no encontrado.'}, status=404)

    if request.method == 'GET':
        return Response(JugadorSerializer(jugador).data)

    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'detail': 'Se requiere administrador.'}, status=403)

    if request.method in ['PUT', 'PATCH']:
        serializer = JugadorSerializer(
            jugador, data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    jugador.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@api_view(['GET'])
def perfil_api(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Autenticación requerida.'}, status=401)
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

