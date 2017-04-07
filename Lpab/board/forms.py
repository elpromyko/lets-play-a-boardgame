from django import forms
from django.contrib.auth import authenticate
from board.models import Genre
from django.core.validators import MinValueValidator, MaxValueValidator


genres = Genre.objects.all()
genre_choices = [(genre.id, genre.name) for genre in genres]

class AuthForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """
        Metoda dorzuca do cleaned_data instacje uzytkownika pod kluczem 'user'
        :return: 
        """
        cleaned_data = super().clean()

        login = cleaned_data['login']
        password = cleaned_data['password']
        user = authenticate(username=login, password=password)
        if user is None:
            raise forms.ValidationError('Bledny login lub haslo')
        cleaned_data['user'] = user
        return cleaned_data

class ChooseCriteriaForm(forms.Form):
    players_number = forms.IntegerField(initial=1, label='players_number', validators=[MinValueValidator(1)])
    genre = forms.ChoiceField(choices=genre_choices, label='genre')
    game_time = forms.IntegerField(label='game_time')

