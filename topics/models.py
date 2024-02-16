from django.db import models

# Create your models here.
class Topic(models.Model):

    PUBLIC_CHOICES = (
        ("public", "공개"),
        ("private", "비공개")
    )

    title = models.TextField()
    public = models.CharField(max_length=20, choices=PUBLIC_CHOICES, default="public")

    def __str__(self):
        return self.title