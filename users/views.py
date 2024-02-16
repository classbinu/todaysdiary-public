from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views
from .forms import SignupForm, MypageForm
from .models import User
from posts.models import Post
import datetime as dt

input = "input input-primary input-bordered my-2"

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    # 비회원 확인
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect("base:index")

    #날짜 가져오기
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date = dt.datetime.now()
        context['year'] = int(date.year) - 14
        context['date'] = date

        return context

class LoginView(auth_views.LoginView):
    template_name = "users/login.html"

    # 비회원 확인
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect("base:index")
    

class MypageUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = User
    template_name = "users/mypage.html"
    fields = [
        "nickname",
        "bio",
        "email",
    ]
    success_url = reverse_lazy("base:mydiary")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["nickname"].widget.attrs={
            "class": input,
            "placeholder": "별명",
            "style": "width: 100%",
        }
        form.fields["bio"].widget.attrs={
            "class": "textarea h-36 textarea-bordered textarea-primary",
            "placeholder": "자기소개",
            "style": "width: 100%;",
        }
        form.fields["email"].widget.attrs={
            "class": input,
            "placeholder": "이메일",
            "style": "width: 100%",
        }
        return form


class BlacklistTemplateView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "base/blacklist.html"
    def get_context_data(self):

        context = super().get_context_data()
        user = get_object_or_404(User, id=self.request.user.id)
        blacklist = user.blacklist.all()
        blacklist_obj = User.objects.filter(id__in=blacklist)
        context["blacklist"] = blacklist_obj

        return context



class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change")

    def get_form(self):
        form = super().get_form()
        form.fields["old_password"].widget.attrs={
            "placeholder": "기존 비밀번호",
            "class": input,
            "style": "width: 100%",
            "minlength": "8",
        }
        form.fields["new_password1"].widget.attrs={
            "placeholder": "새로운 비밀번호",
            "class": input,
            "style": "width: 100%",
            "minlength": "8",
        }
        form.fields["new_password2"].widget.attrs={
            "placeholder": "새로운 비밀번호 확인",
            "class": input,
            "style": "width: 100%",
            "minlength": "8",
        }
        return form


class DropoutView(LoginRequiredMixin, DeleteView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    model = User
    success_url = reverse_lazy("base:index")
    template_name = "users/dropout.html"

    def get_object(self, queryset=None):
        return self.request.user


class FindIdView(View):
    template_name = "users/find_id.html"

    # 비회원 확인
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect("base:index")

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST["id_email"]
        users = User.objects.filter(email=email)

        if users:
            username_list = []

            for user in users:
                username_list.append(user.username)

            subject = "[오늘의 일기] 아이디를 알려드립니다."
            message = f"해당 이메일로 가입된 아이디는 {username_list}입니다."
            sendEmail = EmailMessage(subject, message, to=[email])
            sendEmail.send()
        return render(request, 'users/find_id_done.html')



class BlockedUser(View):

    def post(self, request, *args, **kawrgs):
        blockedUser = request.POST.get('blockedUser')
        username = request.POST.get('blockedUsername')
        user = get_object_or_404(User, id=self.request.user.id)
        user.blacklist.add(blockedUser)
        return redirect("users:blacklist")


class UnblockedUser(View):

    def post(self, request, *args, **kawrgs):
        blockedUser = request.POST.get('blockedUser')
        username = request.POST.get('blockedUsername')
        user = get_object_or_404(User, id=self.request.user.id)
        user.blacklist.remove(blockedUser)
        return redirect("users:blacklist")