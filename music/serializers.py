from rest_framework import serializers
from music.models import Album, Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'album_title', 'artist',
                  'album_logo', 'owner', 'songs']


class AlbumCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['album_title', 'artist', 'album_logo']
