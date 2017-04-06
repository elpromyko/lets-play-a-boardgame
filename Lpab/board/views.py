
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView


from board.models import Game
from .forms import AuthForm, ChooseCriteriaForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, login, logout


import json
import requests
import urllib
import xml.etree.ElementTree as ET
import xml
import urllib.request
import boardgamegeek
from boardgamegeek import BoardGameGeek

class LoginView(View):
    def get(self, request):
        ctx = {'form': AuthForm()}
        return render(request, 'board/login.html', ctx)

    def post(self, request):
        form = AuthForm(data=request.POST) # tu mammy forma z danym z request.POST
        ctx = {'form': form}
        if form.is_valid(): #walidujemy forma
            user = form.cleaned_data['user']
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, 'board/login.html', ctx)

class MainView(View):
    def get(self, request):
        ctx = {'form': ChooseCriteriaForm()}
        return render(request, 'board/index.html', ctx)

    def post(self, request):
        form = ChooseCriteriaForm(data=request.POST)
        if form.is_valid():
            play_num = form.cleaned_data['players_number']
            genre = form.cleaned_data['genre']
            game_time = form.cleaned_data['game_time']
            if play_num == 1:
                games = Game.objects.filter(genre=genre,
                                            max_game_time__lte=game_time,
                                            min_players_number=play_num)
                ctx = {'games': games}

                return render(request, 'board/chosen.html', ctx)

            elif play_num > 1:
                games = Game.objects.filter(max_game_time__lte=game_time,
                                            min_players_number__lte=play_num,
                                            max_players_number__gte=play_num,
                                            genre=genre)

                ctx = {'games': games}
                return render(request, 'board/chosen.html', ctx)
            else:
                pass


class ChooseCriteriaView(View):
    def get(self, request):
        ctx = {'form': ChooseCriteriaForm()}
        return render(request, 'board/criteria.html', ctx)

class ListView(View):
    def get(self, request):
        games = Game.objects.all()
        ctx = {'games': games.order_by('title')}
        return render(request, 'board/list.html', ctx)

class AddGameView(CreateView):
    model = Game
    fields = '__all__'
    success_url = '/'

class DeleteGameView(DeleteView):
    model = Game
    fields = '__all__'
    success_url = '/list'

class GameView(View):

    def get(self, request, game_id):
        form = Game.objects.get(pk=game_id)
        ctx = {'form': form}
        return render(request, 'board/game.html', ctx)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class BggView(View):

    def get(self, request):
        bgg = BoardGameGeek(retries=10, retry_delay=2)
        game = bgg.game("Dominion")
        game_rank = game.id

        ctx = {'game': game_rank}
        return render(request, 'board/bgg.html', ctx)



# class JsonView(View):
#     def get(self, request):
#
#         url = 'https://bgg-json.azurewebsites.net/thing/31260'
#         t = requests.get(url)
#         new_dictionary = t.json()
#         rank = new_dictionary['rank']
#
#         ctx = {'json': rank}
#         return render(request, 'board/json.html', ctx)
#
# class XmlView(View):
#     def get(self, request):
#
#         url = 'https://www.boardgamegeek.com/xmlapi2/search?query=dominion&exact=1&type=boardgame'
#         response = urllib.request.urlopen(url)
#         xml = response.read()
#         root = ET.fromstring(xml)
#
#         ctx = {'xml': root}





