from django.urls import reverse
from django.db import models
from posts.models import Post

# Create your models here.
class Relay(models.Model):

    PUBLIC_CHOICES = (
        ("public", "공개"),
        ("private", "비공개")
    )

    STATUS_CHOICES = (
        ("pending", "진행 중"),
        ("success", "완결"),
        ("failure", "실패")
    )
    
    post = models.ForeignKey(Post, on_delete = models.SET_DEFAULT, related_name="relay", default="0")
    public = models.CharField(max_length=20, choices=PUBLIC_CHOICES, default="public")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.pk