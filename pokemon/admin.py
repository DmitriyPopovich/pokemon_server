
from django.contrib import admin

from pokemon.models import UserPoke


class UserPokeAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', )
    fields = (
        ('pokemon_name', 'owner'),
    )


admin.site.register(UserPoke, UserPokeAdmin)

