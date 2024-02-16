from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.db.models import Q
from .models import Comment
from posts.models import Post
from relays.models import Relay
from topics.models import Topic
from users.models import User

input = "input input-primary input-bordered my-2"
select = "select select-bordered select-primary max-w-xs mx-2"

# Create your views here.
class CommentCreateView(View):

    def post(self, request, *args, **kawrgs):

        post_id = request.POST["post_id"]

        post = get_object_or_404(Post, id=post_id)
        content = request.POST["content"]
        public = request.POST["public"]
        relay = int(request.POST["relay"])
        author = self.request.user
        Comment.objects.create(
            post = post,
            content = content,
            public = public,
            author = author,
        )

        # 릴레이 소설 로직
        if relay > 0:
            comments = Comment.objects.filter(post__id=post_id)
            
            if comments.count() >= 50: #댓글이 50이상이면 릴레이 소설 완결
                content = post.content
                Relay.objects.filter(post__id=post_id).update(status = "success")
                relay_count = Relay.objects.all().count()

                newPost = Post.objects.create(
                    topic=Topic.objects.get(id=1036), #실서버는 id=1036, 테스트 서버는 id=2
                    title=f"릴레이 소설 {relay_count+1}회",
                    content=content,
                    author=User.objects.get(id=1),
                )

                Relay.objects.create(
                    post=newPost,
                )
                
        return redirect('posts:post_detail', pk=post_id)


class CommentDetailView(DetailView):
    pass

class CommentUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Comment
    template_name = "comments/comment_update.html"
    fields = [
        "content",
        "public",
    ]
    def get_success_url(self):
        return reverse_lazy("posts:post_detail", kwargs={"pk": self.object.post.id})
    

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):
        object = self.get_object()
        if object.author != self.request.user:
            raise Http404()
        else:
            return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        return comment

    def get_form(self):
        form = super().get_form()
        form.fields["content"].widget.attrs={
            "class": "textarea h-36 textarea-bordered textarea-primary",
            "style": "width: 100%",
            "maxlength": 180,
        }
        form.fields["public"].widget.attrs={
            "class": "select select-bordered select-primary max-w-xs mx-2"
        }
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 릴레이 소설 객체 가져오기
        pk = self.kwargs["pk"]
        comment = get_object_or_404(Comment, id=pk)
        post = comment.post
        relay = Relay.objects.filter(post__id=post.id)
        if relay.count() == 0:
            relay = None
        else:
            context["relay"] = relay[0]
        
        return context
    

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Comment
    template_name = "comments/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy("posts:post_detail", kwargs={"pk": self.object.post.id})

    # 계정 일치 여부 확인
    def dispatch(self, *args, **kwargs):

        object = self.get_object()

        if object.author == self.request.user:
            return super().dispatch(*args, **kwargs)
        elif object.post.classroom and object.post.classroom.teacher == self.request.user:
            return super().dispatch(*args, **kwargs)
        elif object.post.author == self.request.user:
            return super().dispatch(*args, **kwargs)
        else:
            raise Http404()