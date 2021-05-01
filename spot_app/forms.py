from django import forms


class PlaylistTracksForm(forms.Form):
    playlist_id = forms.CharField()
