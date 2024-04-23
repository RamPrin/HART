from django.urls import path 

from . import views
from . import api_views

urlpatterns = [
    path("", views.choose, name="index"),
    path("king/", views.start, name="king_list"),
    path("king/<int:king_id>/", views.king, name="king"),
    path("king/accept/", views.king_accept, name='accept_servant'),
    path("servant/", views.servant, name="servant_index"),
    path("servant/new/", views.servant_add_html, name="servant_create"),
    path("servant/create/", views.servant_create, name="servant_create_api"),
    path("servant/sign/", views.servant_sign_in, name="servant_sign_in"),
    path("servant/<int:servant_id>/", views.servant_info, name="servant_info"),
    path("stats/", views.stats, name='stats'),
    path("api/kings/", api_views.start_api, name='api_king_list'),
    path("api/king/<int:king_id>/", api_views.api_king, name='api_king'),
    path("api/king/accept/", views.king_accept, name='api_accept_servant'),
    path("api/servant/<int:servant_id>/", api_views.api_servant, name='api_servant'),
    path("api/stats/", api_views.api_stats, name='api_stats')
]
