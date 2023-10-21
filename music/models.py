from django.conf import settings
from django.db import models
from django.urls import reverse


class Album(models.Model):
    album_title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    album_logo = models.ImageField(upload_to='album_cover')
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("music:album_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.album_title} - {self.artist}'


class Song(models.Model):
    song_title = models.CharField(max_length=250)
    album = models.ForeignKey(
        Album, related_name="songs", on_delete=models.CASCADE)
    music_file = models.FileField(upload_to='song', null=True)

    def __str__(self):
        return f'{self.song_title}'
