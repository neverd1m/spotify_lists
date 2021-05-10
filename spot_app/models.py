from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect


# менеждер для фильтра треков, у которых уже есть ссылка на видео.
class VideoManager(models.Manager):
    def get_queryset(self):
        return super().get_query_set().filter(has_video=True)


class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    playlist_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=timezone)

    def __str__(self):
        return f'{self.name}'


class Track(models.Model):
    youtube_id = models.CharField(
        max_length=150, null=True, blank=True, default=None)
    has_video = False
    artist = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    playlist = models.ForeignKey(
        'Playlist', related_name='tracks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    objects = models.Manager()
    video_objects = VideoManager()

    def __str__(self):
        return f'{self.name} by {self.artist}'

    def get_absolute_url(self):
        if not self.youtube_link:
            return None
        return redirect(self.youtube_link)
