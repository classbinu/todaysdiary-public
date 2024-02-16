import os
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .models import Post
from topics.models import Topic
from classrooms.models import Classroom
from comments.models import Comment
from users.models import User
from relays.models import Relay
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import threading
from django.db import close_old_connections

input = "input input-primary input-bordered my-2"
select = "select select-bordered select-primary w-full max-w-xs"


class PostCreateView(LoginRequiredMixin, CreateView, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Post
    fields = [
        "author",
        "topic",
        "title",
        "content",
        "classroom",
        "public",
    ]
    template_name = "posts/post_create.html"
    context_object_name = "classroom_list"

    def get_queryset(self):
        user_id = self.request.user.id
        return Classroom.objects.filter(
            Q(state="open") & (Q(student=user_id) | Q(teacher=user_id))
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_pk = self.request.GET.get("topic", "1")  # 임시로 1
        topic = Topic.objects.get(pk=topic_pk)

        if topic.public == "private":
            raise Http404()  # 작성할 수 없는 주제입니다.로 추후에 변경

        context["topic"] = topic
        # context["topic"] = self.request.GET["topic"]
        return context

    def get_form(self):
        form = super().get_form()
        form.fields["title"].widget.attrs = {
            "class": input,
            "placeholder": "제목",
            "style": "width: 100%",
            "maxlength": "40",
            "autocomplete": "off",
            "id": "id_title",
        }
        form.fields["content"].widget.attrs = {
            "class": input,
            "placeholder": "내용",
            "style": "width: 100%; height: 400px;",
        }
        form.fields["classroom"].widget.attrs = {
            "class": select,
        }
        form.fields["public"].widget.attrs = {
            "class": select,
        }
        return form

    # 인공지능 댓글 생성 파트
    def form_valid(self, form):
        response = super().form_valid(form)
        post = self.object
        if self.object.public == "public":
            print("Generate AI Binu Comment in Background")
            threading.Thread(
                target=self.create_ai_comment_background, args=(post,)
            ).start()
        return response

    # 인공지능 댓글 생성 백그라운드
    def create_ai_comment_background(self, post):
        try:
            close_old_connections()
            self.ai_create_comment(post)
        except Exception as e:
            print(f"Error in AI comment creation: {e}")
        finally:
            close_old_connections()

    # 인공지능 댓글 저장 연동
    def ai_create_comment(self, post):
        ai_binu = User.objects.get(id=7500)  # AI 비누쌤 7500
        ai_generated_comment = self.gen_AI_comment(post)
        Comment.objects.create(post=post, content=ai_generated_comment, author=ai_binu)

    # 랭체인 인공지능 댓글 생성
    def gen_AI_comment(self, post):
        llm = ChatOpenAI(
            openai_api_key="",
            # model_name="gpt-3.5-turbo-1106",
            model_name="gpt-4-0125-preview",
            temperature=0.9,
        )

        nickname = self.request.user.nickname

        user_message = f"# 제목: {post.title} \n # 닉네임: {nickname} \n 내용: {post.content}"
        system_message = """
            # 역할
            * 초등학생이 쓴 글에 친절한 댓글을 달아주는 초등학교 선생님
            * 닉네임은 'AI 비누쌤'

            # 제약 조건
            * 상대방의 닉네임으로 인사를 한다.
            * 감정적으로 공감하고 친절한 답변
            * 적절한 이모지 사용
            * 학생이 글쓰기를 좋아할 수 있도록 긍정적인 피드백
            * 사용자에게 다시 질문하지 않고 무조건 답변을 생성한다.

            # 예시
            안녕, 짹짹이!🤗 'AI 비누쌤'이야. 네가 보내준 편지를 받고 정말 기뻐! 💌🌟
            내년에 중학생 1학년이 된다니, 새로운 시작을 앞두고 있는 너에게 정말 축하해! 중학교 생활은 새로운 친구들을 만나고, 새로운 것들을 배우는 흥미진진한 경험이 될 거야. 네가 중학교에서 새로운 모험을 즐기고, 많은 것을 배우며 성장하는 모습을 상상하니 정말 기대되네. 🎒📚

        """

        prompt = ChatPromptTemplate.from_messages(
            [("system", system_message), ("user", "{input}")]
        )
        ### gpt-3.5-turbo-1106
        # input $0.001 / 1K
        # output $0.002 / 1K

        ### gpt-4-0125-preview
        # input $0.01 / 1K
        # output $ 0.03 / 1K
        chain = prompt.pipe(llm)
        res = chain.invoke({"input": user_message})
        return res.content


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, id=self.request.user.id)
            post = self.kwargs["pk"]
            post_obj = get_object_or_404(Post, id=post)
            blockedUser = get_object_or_404(User, id=post_obj.author.id)
            context = {
                "author": blockedUser,
            }
            if user.blacklist.filter(pk=blockedUser.pk):
                return render(request, "base/blocked.html", context)
            else:
                object = self.get_object()

                user_id = self.request.user.id
                user_classroom = Classroom.objects.filter(
                    Q(student=user_id) | Q(teacher=user_id)
                ).order_by("-created_at")

                if object.author == self.request.user:
                    return super().dispatch(request, *args, **kwargs)
                elif (
                    object.public == "private" and object.author == self.request.user
                ):  # 필요없는 라인?
                    return super().dispatch(request, *args, **kwargs)
                elif object.public == "class" and object.classroom in user_classroom:
                    return super().dispatch(request, *args, **kwargs)
                elif object.public == "public":
                    return super().dispatch(request, *args, **kwargs)
                else:
                    raise Http404()

        # 코드 중복 추후 해결
        else:
            object = self.get_object()

            user_id = self.request.user.id
            user_classroom = Classroom.objects.filter(
                Q(student=user_id) | Q(teacher=user_id)
            ).order_by("-created_at")

            if object.author == self.request.user:
                return super().dispatch(request, *args, **kwargs)
            elif (
                object.public == "private" and object.author == self.request.user
            ):  # 필요없는 라인?
                return super().dispatch(request, *args, **kwargs)
            elif object.public == "class" and object.classroom in user_classroom:
                return super().dispatch(request, *args, **kwargs)
            elif object.public == "public":
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, id=self.request.user.id)
            blacklist = user.blacklist.all()

        pk = self.kwargs["pk"]
        object = self.get_object()
        if self.request.user.is_anonymous:
            comment_list = Comment.objects.filter(
                Q(post_id=pk) & Q(public="public")
            ).order_by("id")
        elif object.author == self.request.user:
            comment_list = Comment.objects.filter(post_id=pk).order_by("id")
        elif object.classroom and object.classroom.teacher == self.request.user:
            comment_list = Comment.objects.filter(
                Q(post_id=pk) & ~Q(author__in=blacklist)
            ).order_by("id")
        else:
            comment_list = Comment.objects.filter(
                (Q(post_id=pk) & Q(public="public") & ~Q(author__in=blacklist))
                | Q(post_id=pk) & Q(author=self.request.user)
            ).order_by("id")

        # 릴레이 소설 객체 가져오기
        relay = Relay.objects.filter(post__id=pk)
        if relay.count() == 0:
            relay = None
        else:
            context["relay"] = relay[0]

        context["comment_list"] = comment_list
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Post
    template_name = "posts/post_update.html"
    fields = [
        "title",
        "content",
        "classroom",
        "public",
    ]

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        object = self.get_object()
        if object.author != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Post, pk=self.kwargs["pk"]).topic
        context["topic"] = topic

        # 학급 리스트 셀렉트 가져오기
        user_id = self.request.user.id
        classroom_list = Classroom.objects.filter(
            Q(state="open") & (Q(student=user_id) | Q(teacher=user_id))
        ).order_by("-created_at")
        context["classroom_list"] = classroom_list
        return context

    def get_form(self):
        form = super().get_form()
        form.fields["title"].widget.attrs = {
            "class": input,
            "placeholder": "제목",
            "style": "width: 100%",
            "maxlength": "40",
            "autocomplete": "off",
        }
        form.fields["content"].widget.attrs = {
            "class": input,
            "placeholder": "내용",
            "style": "width: 100%; height: 400px;",
        }
        form.fields["classroom"].widget.attrs = {
            "class": select,
        }
        form.fields["public"].widget.attrs = {
            "class": select,
        }
        return form


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Post
    success_url = reverse_lazy("base:mydiary")
    template_name = "posts/post_delete.html"

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        object = self.get_object()
        if object.author == self.request.user:
            return super().dispatch(*args, **kwargs)
        elif object.classroom.teacher == self.request.user:
            return super().dispatch(*args, **kwargs)
        else:
            raise Http404()
