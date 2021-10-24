from django.urls import path
from .views import MedalsList, SearchMedal


urlpatterns = [
    path('list/', MedalsList.as_view(), name='list'),
    path('search/', SearchMedal, name='search'),
]