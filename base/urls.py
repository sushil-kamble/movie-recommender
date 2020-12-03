from django.urls import path
from . import views

urlpatterns = [
    # Main Movie Logic
    path('', views.mainPage, name="mainPage"),
    path('home', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('result', views.result_page, name='result'),
    path('all', views.allPage, name='all'),
    path('top100', views.topPage, name='top100'),
    path('genre', views.genrePage, name='genre'),
    path('allseries', views.allSeries, name='allSeries'),
    path('advsearchresults', views.advSearchResults, name='advSearchResults'),

    # User Watchlist
    path('watchlist/', views.watchList, name="watchlist"),
]
