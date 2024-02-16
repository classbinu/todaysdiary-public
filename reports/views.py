from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from reports.models import Report
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.
class ReportFormView(View):

    def post(self, request, *args, **kawrgs):
        type = request.POST["type"]
        ref = request.POST["ref"]
        content = request.POST["content"]

        if request.user.is_authenticated:
            author = self.request.user
        else:
            author = None
            
        Report.objects.create(
            type = type,
            ref = ref,
            content = content,
            author = author,
        )

        if type == "1":
            typeName = "주제 신고"
        elif type == "2":
            typeName = "일기 신고"
        elif type == "3":
            typeName = "댓글 신고"
        elif type == "4":
            typeName = "주제 제안"
        else:
            typeName = "기타"

        subject = f"[오늘의 일기] 리포트 알림({typeName})"
        message = f"({ref}) {content}"
        sendEmail = EmailMessage(subject, message, to=["classbinu@gmail.com"])
        sendEmail.send()

        # return HttpResponse(status=200)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))