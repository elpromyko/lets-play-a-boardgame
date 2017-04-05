from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from board.models import Game
from .forms import AuthForm, ChooseCriteriaForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, login, logout



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
                games = Game.objects.filter(single_player_mode=True,
                                            max_game_time__lte=game_time)
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
        ctx = {'games': games}
        return render(request, 'board/list.html', ctx)

class AddView(CreateView):
    model = Game
    fields = '__all__'
    success_url = 'index'

class DeleteView(View):
    pass

class LogoutView(View):
    pass





