from django.urls import path 

from . import views

urlpatterns = [
    path("", views.choose, name="index"),
    path("king/", views.start, name="king_list"),
    path("king/<int:king_id>/", views.king, name="king"),
    path("king/accept/", views.king_accept, name='accept_servant'),
    path("servant/", views.servant, name="servant_index"),
    path("servant/new/", views.servant_add_html, name="servant_create"),
    path("servant/create/", views.servant_create, name="servant_create_api"),
    path("servant/info/", views.servant_info, name="servant"),
]
