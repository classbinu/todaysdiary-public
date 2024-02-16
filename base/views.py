from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.db.models import Q
from users.models import User
from posts.models import Post
from topics.models import Topic
from comments.models import Comment
from classrooms.models import Classroom
import random
import os


# index는 추후 확장 시 ListView 사용, 현재는 단순 렌더
class IndexView(ListView):
    model = Post
    template_name = "base/index.html"
    paginate_by = 3
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(Q(id="5") | Q(id="3") | Q(id="2"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_count = User.objects.all().count()
        classroom_count = Classroom.objects.all().count()
        post_count = Post.objects.all().count()

        context["user_count"] = user_count
        context["classroom_count"] = classroom_count
        context["post_count"] = post_count
        return context


class MydiaryListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Post
    template_name = "base/mydiary.html"
    paginate_by = 48
    context_object_name = "post_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        author = get_object_or_404(User, id=user_id)
        context["author"] = author
        return context

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.id).order_by("-created_at")


class CommentListView(ListView):
    model = Comment
    template_name = "base/comment.html"
    paginate_by = 48
    context_object_name = "comment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params_username = self.kwargs["username"]
        author = get_object_or_404(User, username=params_username)
        context["author"] = author
        return context

    def get_queryset(self):
        params_username = self.kwargs["username"]
        author = get_object_or_404(User, username=params_username)
        return Comment.objects.filter(
            Q(author=author) & Q(public="public") & Q(post__public="public")
        ).order_by("-created_at")


class MycommentListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Comment
    template_name = "base/mycomment.html"
    paginate_by = 48
    context_object_name = "comment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        author = get_object_or_404(User, id=user_id)
        context["author"] = author
        return context

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user.id).order_by(
            "-created_at"
        )


class MypostCommentListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Comment
    template_name = "base/mypost_comment.html"
    paginate_by = 48
    context_object_name = "comment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        author = get_object_or_404(User, id=user_id)
        context["author"] = author
        return context

    def get_queryset(self):
        post_list = Post.objects.filter(author=self.request.user.id).values_list(
            "id", flat=True
        )
        return Comment.objects.filter(post__in=post_list).order_by("-created_at")


class DiaryListView(ListView):
    model = Post
    template_name = "base/diary.html"
    paginate_by = 48
    context_object_name = "post_list"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, id=self.request.user.id)
            author = self.kwargs["username"]
            blockedUser = get_object_or_404(User, username=author)
            context = {
                "author": blockedUser,
            }
            if user.blacklist.filter(pk=blockedUser.pk):
                return render(request, "base/blocked.html", context)
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params_username = self.kwargs["username"]
        author = get_object_or_404(User, username=params_username)
        context["author"] = author
        return context

    def get_queryset(self):
        params_username = self.kwargs["username"]
        author = get_object_or_404(User, username=params_username)
        return Post.objects.filter(author=author.id, public="public").order_by(
            "-created_at"
        )


class EverydiaryListView(ListView):
    model = Post
    template_name = "base/everydiary.html"
    paginate_by = 48
    context_object_name = "post_list"

    # 랜덤 일기장 방문하기
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     max = User.objects.all().count() #조건 검토 필요
    #     rand = random.randrange(0, max)
    #     rand_user = User.objects.all()[rand] #조건 수정 필요
    #     context["rand_user"] = rand_user
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 베스트 작품
        # bests = [153, 196, 192, 407]
        # best_posts = Post.objects.filter(Q(id=bests[0]) | Q(id=bests[1]) | Q(id=bests[2]) | Q(id=bests[3]))
        # context["best_posts"] = best_posts

        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, id=self.request.user.id)
            blacklist = user.blacklist.all()
            return Post.objects.filter(
                Q(public="public") & ~Q(author__in=blacklist)
            ).order_by("-created_at")
        else:
            return Post.objects.filter(Q(public="public")).order_by("-created_at")


class IntroTemplateView(TemplateView):
    template_name = "base/intro.html"


class NoticeTemplateView(TemplateView):
    template_name = "base/notice.html"


class QnaTemplateView(TemplateView):
    template_name = "base/qna.html"


class ContactTemplateView(TemplateView):
    template_name = "base/contact.html"
