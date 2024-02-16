from keyword import kwlist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password, is_password_usable
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateView
from django.db.models import Q
from django import forms
from .models import Classroom
from users.models import User
from posts.models import Post
from datetime import datetime

input = "input input-primary input-bordered my-2"
select = "select select-bordered select-primary w-full max-w-xs"

class ClassroomListView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Classroom
    template_name = "classrooms/classroom_list.html"
    paginate_by = 16
    context_object_name = "classroom_list"

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.filter(Q(state="open") & (Q(student__in=[user]) | Q(teacher=user))).order_by("-created_at").distinct()


class ClassroomCreateView(LoginRequiredMixin, CreateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Classroom
    fields = [
        "year",
        "school",
        "grade",
        "number",
        "bio",
        "pin",
        "teacher",
    ]
    template_name = "classrooms/classroom_create.html"

    def get_form(self):
        form = super().get_form()
        form.fields["year"].widget.attrs={
            "class": input + " readonly hidden",
            "placeholder": "학년도",
            "value": datetime.today().year,
            "style": "width: 100%",
        }
        form.fields["school"].widget.attrs={
            "class": input,
            "placeholder": "학교명",
            "style": "width: 100%",
            "autocomplete": "off"
        }
        form.fields["grade"].widget.attrs={
            "class": select,
            "placeholder": "학년",
            "style": "width: 100%",
        }
        form.fields["number"].widget.attrs={
            "class": input,
            "placeholder": "반(동아리명)",
            "style": "width: 100%",
            "autocomplete": "off"
        }
        form.fields["bio"].widget.attrs={
            "class": "textarea h-40 textarea-bordered textarea-primary",
            "placeholder": "학급 소개",
            "style": "width: 100%",
        }
        form.fields["pin"].widget.attrs={
            "class": input,
            "placeholder": "학급 비밀번호(숫자 6자리)",
            "style": "width: 100%",
            "pattern": "[0-9]+",
            "minlength": "6",
            "maxlength": "6",
            "autocomplete": "off",
        }
        return form


class ClassroomDetailView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Post
    template_name = "classrooms/classroom_detail.html"
    paginate_by = 12
    context_object_name = "post_list"

    # 학급 가입 여부 확인
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.student.filter(pk=self.request.user.pk).exists() or classroom.teacher == self.request.user:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect("classrooms:classroom_in", pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)
        student_list = classroom.student.all()
        context["classroom"] = classroom
        context["student_list"] = student_list
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Post.objects.filter(classroom=pk).exclude(public="private").order_by("-created_at")


class ClassroomUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Classroom
    template_name = "classrooms/classroom_update.html"
    fields = [
        "school",
        "grade",
        "number",
        "bio",
        "pin",
        "bio",
    ]

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):

        object = self.get_object()

        if object.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요
            
        if object.teacher != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        classroom = get_object_or_404(Classroom, pk=self.kwargs["pk"])
        return classroom

    def get_form(self):
        form = super().get_form()
        form.fields["school"].widget.attrs={
            "class": input,
            "placeholder": "학교명",
            "style": "width: 100%",
            "autocomplete": "off",
        }
        form.fields["grade"].widget.attrs={
            "class": input,
            "placeholder": "학년",
            "style": "width: 100%",
        }
        form.fields["number"].widget.attrs={
            "class": input,
            "placeholder": "반(동아리명)",
            "style": "width: 100%",
            "autocomplete": "off",
        }
        form.fields["bio"].widget.attrs={
            "class": "textarea h-40 textarea-bordered textarea-primary",
            "placeholder": "학급 소개",
            "style": "width: 100%",
        }
        form.fields["pin"].widget.attrs={
            "class": input,
            "placeholder": "학급 비밀번호(숫자 6자리)",
            "style": "width: 100%",
            "pattern": "[0-9]+",
            "minlength": "6",
            "maxlength": "6",
            "autocomplete": "off",
        }
        return form


class ClassroomDeleteView(LoginRequiredMixin, DeleteView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Classroom
    success_url = reverse_lazy("classrooms:classroom_list")
    template_name = "classrooms/classroom_delete.html"
    


    # def post(self, request, *args, **kawrgs):
    #     pk = self.kwargs["pk"]
    #     classroom = get_object_or_404(Classroom, id=pk)
    #     classroom.state = "closed"
    #     classroom.save()

    #     post_list = Post.objects.filter(classroom=pk)
    #     for post in post_list:
    #         post.classroom = None
    #         post.save()
    #     return redirect("classrooms:classroom_list")

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        object = self.get_object()

        if object.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if object.teacher != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)


class ClassroomSearchView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Classroom
    template_name = "classrooms/classroom_search.html"
    paginate_by = 80
    context_object_name = "classroom_list"

    # 학급 서치에 페이지네이션 적용 시 페이지에서 검색 키워드를 가져오지 못하는 문제 있음
    # 한 페이지 객체를 80으로 임시 처방
    # 페이지네이션 템플릿에서 다음 페이지에 해당 검색 조건 주소 가져오면 될 듯

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get("year", "")
        school = self.request.GET.get("school", "")
        context["year"] = year
        context["school"] = school
        return context

    def get_queryset(self):
        year = self.request.GET.get("year", "")
        school = self.request.GET.get("school", "")
        return Classroom.objects.filter(Q(state="open") & (Q(year=year) & Q(school__contains=school))).order_by("-created_at")


class ClassroomInView(LoginRequiredMixin, View):
    
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "classrooms/classroom_in.html"

    def get(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.student.filter(pk=request.user.pk).exists():
            return redirect("classrooms:classroom_detail", pk)
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)
        pin = classroom.pin
        input_pin = request.POST["pin"]
        if pin == input_pin:
            classroom.student.add(request.user)
            return redirect("classrooms:classroom_detail", pk)
        else:
            return redirect("classrooms:classroom_failed")


class ClassroomFailedView(TemplateView):
    template_name = "classrooms/classroom_failed.html"



class ClassroomOutView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "classrooms/classroom_out.html"

    def get(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.student.filter(pk=request.user.pk).exists():
            return render(request, self.template_name)
        else:
            return redirect("base:index") #에러메시지 송출 필요

    def post(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)
        classroom.student.remove(request.user)
        return redirect("classrooms:classroom_list")


class ClassroomMemberView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = User
    template_name = "classrooms/classroom_member.html"
    paginate_by = 80
    context_object_name = "classroom_list"

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.teacher != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)
        student_list = classroom.student.all()
        context["classroom"] = classroom
        context["student_list"] = student_list
        return context


class ClassroomPasswordView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "classrooms/classroom_password.html"

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.teacher != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kawrgs):
        return render(request, self.template_name)

    def post(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        id = self.request.GET["id"]
        # classroom = get_object_or_404(Classroom, id=pk)
        password = self.request.POST["password"]
        password1 = self.request.POST["password1"]
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            password = make_password(password)
            user = User.objects.filter(id=id)
            user.update(password=password)

        return redirect(f"/classroom/{pk}/member/")


class ClassroomBanView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "classrooms/classroom_ban.html"

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        classroom = get_object_or_404(Classroom, id=pk)

        if classroom.state == "closed":
            raise Http404() #폐쇄된 학급입니다. 수정 필요

        if classroom.teacher != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)


    def get(self, request, *args, **kawrgs):
        return render(request, self.template_name)


    def post(self, request, *args, **kawrgs):
        pk = self.kwargs["pk"]
        id = self.request.GET["id"]
        classroom = get_object_or_404(Classroom, id=pk)
        ban_user = classroom.student.get(id=id)
        classroom.student.remove(ban_user)
        return redirect(f"/classroom/{pk}/member/")