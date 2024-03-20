from django.urls import path 

from . import views

urlpatterns = [
    path("", views.choose, name="index"),
    path("king/", views.start, name="king_list"),
    path("king/<int:king_id>/", views.king, name="king"),
    path("servant/", views.serve, name="servant_create")
]
