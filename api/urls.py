from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.playlist_list),
    path("list/<int:id>/", views.playlist_detail),
    path("music/", views.music_list),
    path("music/<int:id>/", views.music_detail),
    path("music/<int:id>/file", views.music_file),
]
