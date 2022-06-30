# Generated by Django 4.0.5 on 2022-06-29 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokemon', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpoke',
            options={'verbose_name': 'Pokemon', 'verbose_name_plural': 'Pokemons'},
        ),
        migrations.AlterField(
            model_name='userpoke',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pokemons', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]