from secrets import youtube_api
import requests

user_token = 'BQDE_o22r60qafyHg_3mWaRE_HwFlPGL9uPoLrK5xmLyNm2dbZaofXxU6HArJ0FrvHsvS_QPQCnjf4gnvZeL-7SE1qFOZVsRaXSXOJq1W1BMP-tCu6E_hGxOmJhpnv3T8uCeT_DbdQwafcDey91VLu_jPhf-nY5f84OhIEvmWGMHdwnnxlnA5QA2BSVwzg'
# items_from_playlists_token = 'BQCj_iqc5L1OmlTNl5ZVCgaArtVkB1DzgMorOSJ_N_ZVUzCekKeegW7cuNhqSp45PeiHG0xZO3g-UbRrgZKO00t8pOc7FbQlMuOfTd0A36KM8XlOsZv0wu_T1siQUNkS1H1NIXgb2SItl-7wcfIP1gpQA9rCbtEqR6zUamTSpjHnBJOuv_CvZ26rN4hQqw'
user_id = '1foud0u3flnlgdbks2lbg6rld'
playlist_id = "37i9dQZF1DX8z1UW9HQvSq"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {user_token}"
}


# def get_user_playlists(user_id=None):
#     query = 'https://api.spotify.com/v1/me/playlists'
#     if user_id:
#         query = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'

#     response = requests.get(query, headers=headers).json()
#     playlists_list = response["items"][0]
#     return playlists_list['name'], playlists_list['id']


# def get_tracks(playlist_id):
#     payload = {
#         "market": "RU"
#     }
#     if not playlist_id:
#         raise ExceptionError(
#             'Ты просишь треки, но ты просишь их без id плейлиста.')

#     query = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
#     response = requests.get(query, headers=headers, params=payload).json()

#     tracks_results_gen = ((track['track']['name'], track['track']
#                            ['album']['artists'][0]['name']) for track in response['items'])

#     return tracks_results_gen


# for track in get_tracks("37i9dQZF1DX8z1UW9HQvSq"):
#     print(track)
# payload = {
#     # 'chart': 'mostPopular',
#     'key': f'{youtube_api}',
#     'regionCode': 'RU'
# }
# request = requests.get(
#     'https://www.googleapis.com/youtube/v3/videoCategories', params=payload).json()
# response = ((item['etag'], item['id'], item['snippet']['title'])
#             for item in request['items'])
# print(list(response))


payload_for_search = {
    'part': 'snippet',
    'type': 'video',
    'q': 'Deftones | Ceremony',
    'videoCategoryId': '10',
    'maxResults': 1,
    'key': f'{youtube_api}'
}
request = requests.get(
    'https://www.googleapis.com/youtube/v3/search', params=payload_for_search).json()
videoId = request['items'][0]['id']['videoId']
uri = 'https://www.youtube.com/watch?v=' + videoId

# Запрос get_playlists_items не содержит в ответе имени плейлиста, зато неожиданно все нужное есть в get_playlist.

# tracks_data = sp.playlist_items(
#     playlist_id, offset=0, fields='items.track.name, items.track.album.artists', market='RU', additional_types=['track'])
# print(tracks_data)
# tracks_data = ((item['track']['name'], item['track']
#                 ['album']['artists'][0]['name']) for item in tracks_data['items'])
