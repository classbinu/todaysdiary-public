from django.db import models
from users.models import User

class Report(models.Model):

    TYPE_CHOICES = (
        ("1", "주제 신고"),
        ("2", "일기 신고"),
        ("3", "댓글 신고"),
        ("4", "주제 제안"),
        ("5", "기능 제안"),
        ("0", "기타"),
    )

    STATE_CHOICES = (
        ("open", "접수"),
        ("closed", "완료"),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False)
    ref = models.CharField(max_length=10, blank=True)
    content = models.TextField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete = models.SET_DEFAULT, default="", blank=True, related_name="report")
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    # def get_absolute_url(self):
    #     return reverse("classrooms:classroom_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.content
