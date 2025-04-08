from django.db import models


class MusicModel(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    duration = models.FloatField()
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.artist} - {self.title}"


class PlaylistModel(models.Model):
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(MusicModel)

    def __str__(self):
        return f"{self.name} ({self.songs.count()})"
