from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    pic = models.ImageField(upload_to="pic", blank=True)
    bio = models.TextField(max_length=200, blank=True)
    point = models.IntegerField(default=0)
    first_name = None
    last_name = None
    blacklist = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.username