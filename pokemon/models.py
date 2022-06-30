from django.db import models


class UserPoke(models.Model):
    pokemon_name = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(
        "users.AdvUser",
        on_delete=models.PROTECT,
        verbose_name='owner',
        related_name='pokemons'
    )

    class Meta:
        db_table = "pokemon"
        verbose_name = 'Pokemon'
        verbose_name_plural = 'Pokemons'

    def __str__(self):
        return self.pokemon_name
