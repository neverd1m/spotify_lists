from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, View, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from functools import wraps
import json
from .forms import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from .secrets import user_id, user_token, youtube_api

from .models import *


class Playlists(ListView):
    queryset = Playlist.objects.all().order_by('created_at')
    template_name = 'main_app/show_playlists.html'
    paginate_by = 10
    context_object_name = 'playlists'


class Tracks(ListView):
    template_name = 'main_app/show_tracks.html'
    paginate_by = 10
    context_object_name = 'tracks'

    def get_queryset(self):
        playlist = Playlist.objects.get(playlist_id=self.kwargs["playlist_id"])
        return playlist.tracks.all().order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = Playlist.objects.get(playlist_id=self.kwargs["playlist_id"])
        context["playlist"] = playlist
        return context


def get_user_playlists(request, user_id=None):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))
    if not user_id:
        playlists = sp.current_user_playlists(offset=0)
        playlists = [(item['name'], item['id'])
                     for item in playlists['items']]

    else:
        playlists = sp.user_playlists(user_id, offset=0)
        playlists = ((item['name'], item['id'])
                     for item in playlists['items'][0])
    for name, pl_id in playlists:
        Playlist.objects.get_or_create(name=name, playlist_id=pl_id)

    return redirect(reverse('playlists'))


class PlaylistTracks(View):

    def get(self, request, custom=False, *args, **kwargs):
        form = PlaylistTracksForm()
        return render(request, 'main_app/custom_playlists.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = PlaylistTracksForm(request.POST)
        if form.is_valid():
            playlist_id = form.cleaned_data['playlist_id']
            playlist_tracks = get_playlist_tracks(request,
                                                  playlist_id=playlist_id, custom=True)
            tracks = (get_links(request, name=name, artist=artist)
                      for name, artist in playlist_tracks[0])

        return render(request, 'main_app/custom_playlists.html', context={'form': form, 'tracks': tracks, 'playlist_name': playlist_tracks[1]})


def get_playlist_tracks(request, playlist_id=None, custom=False):
    # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))
    tracks_data = sp.playlist(
        playlist_id, fields='name, id, tracks.items.track.name, tracks.items.track.album.artists', market='RU', additional_types=['track'])

    playlist_name, playlist_id = tracks_data['name'], tracks_data['id']
    tracks_data = ((item['track']['name'], item['track']
                    ['album']['artists'][0]['name']) for item in tracks_data['tracks']['items'])
    if custom:
        return (list(tracks_data), playlist_name, playlist_id)
    playlist_model = Playlist.objects.get(playlist_id=playlist_id)

    for name, artist in tracks_data:
        Track.objects.get_or_create(
            name=name, artist=artist, playlist=playlist_model)

    return redirect(reverse('playlist_tracks', kwargs={"playlist_id": playlist_id}))


def get_links(request, name=None, artist=None, playlist_id=None):
    payload = {
        'part': 'snippet',
        'type': 'video',
        'q': f'{name} {artist} official',
        'videoCategoryId': '10',
        'maxResults': 1,
        'key': f'{youtube_api}'
    }
    if playlist_id:
        playlist = Playlist.objects.get(playlist_id=playlist_id)
        for track in playlist.tracks.all():
            payload['q'] = f'{track.name} {track.artist}'
            request_attempt = requests.get(
                'https://www.googleapis.com/youtube/v3/search', params=payload).json()
            videoId = request_attempt['items'][0]['id']['videoId']
            uri = 'https://www.youtube.com/watch?v=' + videoId
            track.youtube_link = uri
            track.has_video = True
            track.youtube_id = videoId
            track.save()
        return redirect(reverse('playlist_tracks', kwargs={"playlist_id": playlist_id}))

    else:
        request_attempt = requests.get(
            'https://www.googleapis.com/youtube/v3/search', params=payload).json()
        try:
            videoId = request_attempt['items'][0]['id']['videoId']
            uri = 'https://www.youtube.com/watch?v=' + videoId
        except:
            videoId = None
            uri = None

    return (name, artist, uri, videoId)
