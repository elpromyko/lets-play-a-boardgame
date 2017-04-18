from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from board.models import Game
from .forms import AuthForm, ChooseCriteriaForm
from django.urls import reverse
from django.contrib.auth import login, logout
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
            games = Game.objects.filter(max_game_time__lte=game_time,
                                        min_players_number__lte=play_num,
                                        max_players_number__gte=play_num,
                                        genre=genre)
            ctx = {'games': games}

            return render(request, 'board/chosen.html', ctx)

        else:
            ctx = {'form': ChooseCriteriaForm(),
                   'invalid_data': "Wpisz poprawne dane"}

            return render(request, 'board/index.html', ctx)


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
        title_en = form.title_en

        try:
            bgg = BoardGameGeek(retries=10, retry_delay=2)
            game = bgg.game(title_en)
            game_rank = game.ranks
            game_rank_dict = game_rank[0]
            rank = game_rank_dict['value']

            ctx = {'form': form,
                   'game_rank': rank}
            return render(request, 'board/game.html', ctx)

        except AttributeError:
            rank = "n/a"
            ctx = {'form': form,
                   'game_rank': rank}
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