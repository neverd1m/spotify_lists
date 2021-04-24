from django.db import models
from django.conf import settings

# Create your models here.


class Response_list(models.Model):
    requested_data = models.CharField(
        ("Исходный запрос"), max_length=200, blank=False)
    request_date = models.DateTimeField(
        ("Дата запроса"), auto_now=False, auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=("Владелец запроса"), on_delete=models.CASCADE)
    result_list = models.TextField(("Ссылки на видео?"))

    def __str__(self):
        return self.requested_data
