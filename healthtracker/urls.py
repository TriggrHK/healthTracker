from django.urls import path
from .views import *

urlpatterns = [
    path("", indexPageView, name="index"),
    path("account", accountPageView, name="account"),
    path("stats", statsPageView, name="stats"),
    path("journal", journalPageView, name="journal"),
    path("recommendation", recommendationPageView, name="recommendation"),
    path("login", loginPageView, name='login'),

    path("login/login", loginAccount, name='loginAccount'),
    path("login/createAccount", createAccount, name='create'),
    path("login/logout", logout, name='logout'),
    
    path("addFood", addFood, name='addFood'),
    path("addJournal", addJournal, name='addJournal'),

    path("addComo", addComo, name='addComo'),
    path("addAllergy", addAllergy, name='addAllergy'),
    path("editComo", editComo, name='editComo'),
    path("editAllergy", editAllergy, name='editAllergy'),
    path("deleteComo", deleteComo, name='deleteComo'),
    path("deleteAllergy", deleteAllergy, name='deleteAllergy'),
]