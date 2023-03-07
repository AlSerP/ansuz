from django.db import models
from django.contrib.auth.models import AbstractUser


# def directory_path(instance, filename):
#     return f'user_{instance.id}/avatar/{filename}'


class CustomUser(AbstractUser):
    score = models.IntegerField(default=0)
    email = models.EmailField(unique=False, default='-')

    # class Meta(object):
    #     unique_together = ('username',)

    def __str__(self):
        return self.username

