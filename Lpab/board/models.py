from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=128, verbose_name='Tytuł')
    title_en = models.CharField(max_length=128, verbose_name='Tytuł ang')
    min_players_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(9)], verbose_name='Minimalna liczba graczy')
    max_players_number = models.IntegerField(verbose_name='Maksymalna liczba graczy', validators=[MinValueValidator(1), MaxValueValidator(9)])
    genre = models.ForeignKey(Genre, max_length=32, verbose_name='Gatunek')
    max_game_time = models.IntegerField(verbose_name='Czas gry (w min)', validators=[MinValueValidator(1)])
    model_pic = models.ImageField(upload_to='board/static/', default='board/static/no-image-icon.jpg', verbose_name='Okładka')







