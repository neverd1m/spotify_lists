from django.shortcuts import render
from .models import *
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from .secrets import user_id, user_token


# def get_track_from_playlist(request, playlist_id=None):
#     if not playlist_id:
#         raise ExceptionError('Ты не засунул id плейлиста, мужик')

#     playlists = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks',
#                              headers={authorization: 'Bearer items_from_saved_token,
#                                       applica
#                                       })
#     search = requests.get('')


# class PlaylistHandler:
#     user_id = user_id
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {user_token}"
#     }

#     def __init__(self, user_id=None):
#         if not user_id:
#             self.user_id = user_id

#     def get_user_playlists(self, user_id=None):
#         query = "https://api.spotify.com/v1/me/playlists"
#         if user_id:
#             self.user_id = user_id
#             query = "https://api.spotify.com/v1/users/" + self.user_id + "/playlists"
#         response = requests.get(query, headers=self.headers).json()
#         playlists_list = response['items'][0]

#         return playlists_list['name'], playlists_list['id']

# @classmethod
# def get_tracks(cls, playlist_id):
#     payload = {
#         "market": "RU"
#     }
#     if not playlist_id:
#         raise ExceptionError(
#             'Ты просишь треки, но ты просишь их без id плейлиста.')
#     query = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
#     response = requests.get(
#         query, headers=cls.headers, params=payload).json()
#     tracks_results_gen = ((track['track']['name'], track['track']
#                        ['album']['artists'][0]['name']) for track in response['items'])

#     return tracks_results_gen


# Create your views here.


# def index(request):
#     searches = Response_list.objects.filter(user=request.user)
#     return render(request, 'main_app/index.html', context={'searches': searches})

def get_user_playlists(request, user_id=None):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))
    if not user_id:
        playlists = sp.current_user_playlists(offset=0)
        playlists = [(item['name'], item['id'])
                     for item in playlists['items']]

        print(list(playlists))
        return render(request, 'main_app/show_playlists.html', context={'playlists': playlists})

    playlists = sp.user_playlists(user_id, offset=0)
    playlists = [(item['name'], item['id']) for item in playlists['items'][0]]

    return render(request, 'main_app/show_playlists.html', context={'playlists': playlists})


def get_playlist_tracks(request, playlist=None):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    if not playlist:
        tracks_data = sp.current_user_saved_tracks(market=RU)
        print(tracks_data)
        return render(request, 'main_app/search_result.html', context={'tracks': tracks_tracks})

    tracks_data = sp.playlist_items(
        playlist, offset=0, fields='items.track.name,items.track.album.artists[0].name', additional_types=['track'])
    print(tracks_data)

    return render(request, 'main_app/show_tracks.html', context={'tracks': tracks_data})
