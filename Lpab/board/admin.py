from django.contrib import admin

from board.models import Game, Genre


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_players_number', 'max_players_number', 'genre', 'max_game_time', 'single_player_mode']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']