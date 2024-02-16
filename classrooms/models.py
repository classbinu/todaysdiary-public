from django.db import models
from users.models import User
from django.urls import reverse, reverse_lazy

# Create your models here.
class Classroom(models.Model):

    GRADE_CHOICES = (
        ("", "학년을 선택하세요."),
        ("1", "1학년"),
        ("2", "2학년"),
        ("3", "3학년"),
        ("4", "4학년"),
        ("5", "5학년"),
        ("6", "6학년"),
        ("동아리", "동아리"),
    )

    STATE_CHOICES = (
        ("open", "정상"),
        ("closed", "삭제"),
    )

    year = models.CharField(max_length=4)
    school = models.CharField(max_length=20)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=False)
    number = models.CharField(max_length=20)
    pic = models.ImageField(upload_to="pic", blank=True)
    bio = models.TextField(max_length=200, blank=True)
    pin = models.CharField(max_length=6)
    student = models.ManyToManyField(User, blank=True, related_name="classroom")
    teacher = models.ForeignKey(User, on_delete = models.CASCADE, related_name="homeroom")
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("classrooms:classroom_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"[{self.year}] {self.school} {self.grade}-{self.number}"