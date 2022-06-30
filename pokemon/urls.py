from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    path('list/', views.listpoke, name='list_poke'),
    path('add/', views.poke_add, name='add_poke'),
    path('list-users-poke/', views.list_users_poke, name='list_users_poke'),

]