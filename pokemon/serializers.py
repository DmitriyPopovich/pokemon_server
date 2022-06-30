from rest_framework import serializers
from pokemon.models import UserPoke
from users.models import AdvUser


class PokeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoke
        fields = ('pk', 'pokemon_name', 'owner')


class UserPokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoke
        fields = ('pokemon_name',)


class ListUserPokeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    pokemons = UserPokeSerializer(many=True)

    class Meta:
        model = AdvUser
        fields = ('email', 'pokemons')