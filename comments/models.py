from django.urls import reverse
from django.db import models
from users.models import User
from posts.models import Post

# Create your models here.
class Comment(models.Model):

    PUBLIC_CHOICES = (
        ("public", "공개"),
        ("private", "비공개")
    )
    
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="post_commnet")
    content = models.TextField()
    public = models.CharField(max_length=20, choices=PUBLIC_CHOICES, default="public")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content