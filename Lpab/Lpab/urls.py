"""Lpab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from board.views import LoginView, MainView, ListView, AddGameView, LogoutView, \
    GameView, DeleteGameView, BggView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^list$', ListView.as_view(), name='list'),
    url(r'^add$', AddGameView.as_view(), name='add'),
    url(r'^delete/(?P<pk>(\d)+)$', DeleteGameView.as_view(), name='delete'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^game/(?P<game_id>(\d)+)', GameView.as_view(), name="game"),
    url(r'^bgg$', BggView.as_view(), name='bgg'),
]
