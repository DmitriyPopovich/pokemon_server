from django.urls import reverse
from rest_framework import status
from users.models import AdvUser
from rest_framework.test import APIClient, APITestCase
from unittest.mock import Mock


class UserPokeTests(APITestCase):

    def setUp(self):
        """"
            create default user and add pokemon for user
        """
        data_user = {"user": {"email": "poke@test.com", "password": "poke", "password2": "poke"}}
        data_pokemon_for_user = {'pokemon': {'pokemon_name': 'bulbasaur'}}
        self._create_user(data_user)
        client = self._get_api_client()
        url_add_pokemon = reverse('poke:add_poke')
        client.post(url_add_pokemon, data_pokemon_for_user, format='json')

    def _create_user(self, data):
        url = reverse('user:registration')
        response = self.client.post(url, data)
        return response

    @staticmethod
    def _get_tmp_user():
        return AdvUser.objects.get(email='poke@test.com')

    def _get_credentials(self):
        tmp_user = self._get_tmp_user()
        return tmp_user.token

    def _get_api_client(self):
        token = self._get_credentials()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return client

    def test_add_pokemon_for_user(self):
        """
            Test add pokemon for user
        """
        client = self._get_api_client()
        url = reverse('poke:add_poke')
        data = {'pokemon': {'pokemon_name': 'charmeleon'}}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['pokemon_name'], 'charmeleon')

    def test_show_users_pokemons(self):
        """
            Test add pokemon for user
        """
        client = self._get_api_client()
        url = reverse('poke:list_users_poke')
        response = client.get(url)
        tmp_pokemon_name = response.data[0]['pokemons'][0]['pokemon_name']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tmp_pokemon_name, 'bulbasaur')

    def test_list_all_pokemons(self):
        """
            Test list all pokemons
        """
        url = reverse('poke:list_poke')
        client = self._get_api_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1154)

    def test_list_all_pokemons_with_mock(self):
        """
            Test list all pokemons with mock data
        """
        url = reverse('poke:list_poke')
        mock_data = {
            "success": 1,
            "pokemons": {
                "count": 2,
                "results": [
                    {
                        "name": "bulbasaur",
                        "url": "https://pokeapi.co/api/v2/pokemon/1/"
                    },
                    {
                        "name": "ivysaur",
                        "url": "https://pokeapi.co/api/v2/pokemon/2/"
                    }
                ]
            }
        }
        client = self._get_api_client()
        client.get = Mock()
        client.get.return_value = mock_data
        response = client.get(url)
        self.assertEqual(response['pokemons']['count'], 2)