from django.urls import path 

from . import views

urlpatterns = [
    path("", views.choose, name="index"),
    path("king/", views.start, name="king_list"),
    path("king/<int:king_id>/", views.king, name="king"),
    path("servant/", views.servant, name="servant_index"),
    path("servant/new/", views.servant_new, name="sevant_new"),
    path("servant/<int:servant_id>/", views.servant_info, name="servant")
]
