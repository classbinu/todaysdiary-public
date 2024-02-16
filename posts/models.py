from django.urls import reverse
from django.db import models
from users.models import User
from topics.models import Topic
from classrooms.models import Classroom

# Create your models here.
class Post(models.Model):

    PUBLIC_CHOICES = (
        ("public", "모두 공개"),
        ("class", "우리반 공개"),
        ("private", "비공개")
    )
    
    topic = models.ForeignKey(Topic, on_delete = models.SET_DEFAULT, related_name="topic", default="0")
    title = models.CharField(max_length=80)
    content = models.TextField()
    classroom = models.ForeignKey(Classroom, on_delete = models.SET_NULL, null=True, blank=True)
    public = models.CharField(max_length=20, choices=PUBLIC_CHOICES, default="public")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="post")
    hits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    #템플릿에서 사용할 수 있음
    @property
    def hits_up(self):
        self.hits +=1
        self.save()
        return self.hits

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title