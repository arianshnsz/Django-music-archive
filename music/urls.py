from django.urls import path

from music import views
app_name = 'music'

urlpatterns = [
    # urls for template
    path('', views.AlbumList.as_view(), name='index'),
    path('album/<int:pk>/', views.AlbumDetail.as_view(), name='album_detail'),
    path('album/add/', views.AlbumCreate.as_view(), name='album_add'),
    path('album/<int:pk>/update/',
         views.AlbumUpdate.as_view(), name='album_update'),
    path('album/<int:pk>/add/', views.SongCreate.as_view(), name='add_song'),
    path('album/<int:pk>/delete/',
         views.AlbumDelete.as_view(), name='album_delete'),
    path('music/song/<int:pk>/delete/',
         views.SongDelete.as_view(), name='song_delete'),
    # urls for API
    path('api/', views.AlbumListAPI.as_view()),
    path('api/album/add/', views.AlbumCreateAPI.as_view()),
    path('api/album/<int:pk>/', views.AlbumDetailAPI.as_view()),
    path('api/song/add/', views.SongCreateAPI.as_view()),

    path('toggle_playback/<int:song_id>/',
         views.TogglePlaybackView.as_view(), name='toggle_playback'),
]
