from django.contrib import admin
from music.models import Album, Song


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['artist', 'album_title', 'owner']


class SongAdmin(admin.ModelAdmin):
    list_display = ['song_title', 'album']


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
