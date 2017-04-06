from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput

class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=128, verbose_name='Tytuł')
    title_en = models.CharField(max_length=128, verbose_name='Tytuł ang')
    min_players_number = models.IntegerField(verbose_name='Minimalna liczba graczy')
    max_players_number = models.IntegerField(verbose_name='Maksymalna liczba graczy')
    genre = models.ForeignKey(Genre, max_length=32, verbose_name='Gatunek')
    max_game_time = models.IntegerField(verbose_name='Czas gry (w min)')
    model_pic = models.ImageField(upload_to='board/static/', default='board/static/no-image-icon.jpg', verbose_name='Okładka')
    # single_player_mode = models.BooleanField(default=False, verbose_name='Dla jednego gracza')







