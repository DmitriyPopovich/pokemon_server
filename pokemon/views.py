from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from users.models import AdvUser
from .models import UserPoke
from .renderers import PokeJSONRenderer, UserPokeJSONRenderer
from .serializers import PokeAddSerializer, ListUserPokeSerializer
from .services import get_data


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((PokeJSONRenderer,))
def listpoke(request):
    try:
        poke_list = get_data('pokemon')
    except:
        poke_list = {"errors": {"error": "No internet connection"}}
    return Response(poke_list, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((PokeJSONRenderer,))
def poke_add(request):
    pokemon = request.data.get('pokemon', {})
    pokemon['owner'] = request.user.pk
    custom_error = {}
    poke_from_api = {}

    exists_pokemon_for_user = UserPoke.objects.filter(pokemon_name=pokemon['pokemon_name'], owner=request.user.id)
    if exists_pokemon_for_user:
        msg = 'Pokemon {} already added for user {}'.format(pokemon['pokemon_name'], request.user.email)
        custom_error = {"errors": {"error": msg}}
    try:
        poke_from_api = get_data('pokemon', pokemon['pokemon_name'])
    except:
        custom_error = {"errors": {"error": "Unknown pokemon"}}

    serializer = PokeAddSerializer(data=pokemon, many=False)
    if serializer.is_valid() and not exists_pokemon_for_user and poke_from_api:
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        if serializer.errors:
            data = {"errors": serializer.errors}
        else:
            data = custom_error
        return Response(data, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((UserPokeJSONRenderer,))
def list_users_poke(request):
    pokemon_user_data = AdvUser.objects.filter(is_superuser=False)
    serializer_user_poke = ListUserPokeSerializer(pokemon_user_data, many=True)
    return Response(serializer_user_poke.data, status=HTTP_200_OK)
