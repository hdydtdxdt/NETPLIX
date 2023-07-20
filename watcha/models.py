from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    story = models.TextField()
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=-1)
    voter = models.ManyToManyField(User, related_name='voter_movie')  # 추천인 추가
    def __str__(self):
        return self.title
