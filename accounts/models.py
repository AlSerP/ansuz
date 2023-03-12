from django.db import models
from django.contrib.auth.models import AbstractUser
from tasks.models import Task


# def directory_path(instance, filename):
#     return f'user_{instance.id}/avatar/{filename}'


class CustomUser(AbstractUser):
    score = models.IntegerField(default=0)
    email = models.EmailField(unique=False, default='-')

    # class Meta(object):
    #     unique_together = ('username',)

    def __str__(self):
        return self.username

    def add_score(self, score):
        self.score += score
        self.save()

    def update_score(self):
        self.score = 0
        tasks = Task.objects.all()
        for task in tasks:
            self.add_score(task.get_best_mark(self))
