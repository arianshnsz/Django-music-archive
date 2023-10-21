from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from music.models import Album, Song
from music import serializers

import signal
import subprocess

vlc_process = None  # Store the VLC process
is_paused = False
current_song_id = None  # Store the ID of the currently playing song


class AlbumList(LoginRequiredMixin, generic.ListView):
    model = Album
    context_object_name = 'all_albums'
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


class AlbumDetail(LoginRequiredMixin, generic.DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'music/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.get_object().songs.all()
        return context


class AlbumCreate(LoginRequiredMixin, generic.CreateView):
    model = Album
    fields = ['artist', 'album_title', 'album_logo']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'album_logo']


class AlbumDelete(LoginRequiredMixin, generic.DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongCreate(LoginRequiredMixin, generic.CreateView):
    model = Song
    fields = '__all__'

    def get_initial(self):
        initial_data = super(SongCreate, self).get_initial()
        album = Album.objects.get(id=self.kwargs.get('pk'))
        initial_data['album'] = album
        return initial_data

    def get_success_url(self):
        album = Album.objects.get(id=self.kwargs.get('pk'))
        return album.get_absolute_url()


class SongDelete(LoginRequiredMixin, generic.DeleteView):
    model = Song

    def get_success_url(self):
        album = Song.objects.get(id=self.kwargs.get('pk')).album
        return album.get_absolute_url()


class AlbumListAPI(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


class AlbumCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.AlbumCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()

    serializer_class = serializers.AlbumSerializer


class SongCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.SongSerializer

# for playing locally


class TogglePlaybackView(View):
    def post(self, request, song_id, *args, **kwargs):
        global vlc_process, is_paused, current_song_id

        song = Song.objects.get(pk=song_id)

        if current_song_id == song_id:
            if vlc_process and not is_paused:
                vlc_process.send_signal(signal.SIGSTOP)  # Pause the playback
                is_paused = True
                status = 'paused'
            elif vlc_process and is_paused:
                vlc_process.send_signal(signal.SIGCONT)  # Resume the playback
                is_paused = False
                status = 'resumed'
            else:
                vlc_command = ['vlc', song.music_file.path]
                vlc_process = subprocess.Popen(vlc_command)
                is_paused = False
                status = 'playing'
        else:
            # Stop the currently playing song
            if vlc_process:
                vlc_process.terminate()
                vlc_process = None
                is_paused = False

            # Start the new song
            vlc_command = ['cvlc', song.music_file.path]
            vlc_process = subprocess.Popen(vlc_command)
            is_paused = False
            status = 'playing'

        # Update the currently playing song
        current_song_id = song_id

        referring_page = request.META.get('HTTP_REFERER', '/')
        return redirect(referring_page)