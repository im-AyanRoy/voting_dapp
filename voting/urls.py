from django.urls import path
from . import views

urlpatterns = [
    path('', views.voting_page, name="voting_page"),
    path('get_candidates/', views.get_candidates, name="get_candidates"),
    path('vote/', views.vote, name="vote"),
]
