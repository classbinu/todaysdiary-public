from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.shortcuts import render
from django.db.models import Q
from users.models import User
from posts.models import Post
from topics.models import Topic
from comments.models import Comment
import random
import csv

# Create your views here.
class TopicListView(ListView):
    model = Post
    template_name = "topics/topic.html"
    paginate_by = 8
    context_object_name = "post_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_id = Topic.objects.last().id

        topic = None
        while topic == None:
            # rand = 573
            rand = random.randrange(1, int(last_id) + 1)
            # topic model id 공백으로 인한 임시 예외 처리
            if rand > 1061 and rand < 1094:
                continue
            
            topic = Topic.objects.get(id=rand)
            if topic.public == "private":
                topic = None
            
        context["topic"] = topic
        context["ad"] = rand % 3

        post_list = Post.objects.filter(Q(public="public") & Q(topic=topic)).order_by("-created_at")
        context["post_list"] = post_list
        return context


class FirstView(View):
    pass
    
    # def get(self, request, *args, **kawrgs):
    #     f = open('static/topics.csv', 'r', encoding='utf-8')
    #     rdr = csv.reader(f)
    #     for line in rdr:
    #         print(line[0])
    #         t = Topic(title=line[0])
    #         t.save()
    #     f.close()

    #     return redirect("base:index")