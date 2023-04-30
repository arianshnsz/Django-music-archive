from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics

from music.models import Album, Song
from music import serializers


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
