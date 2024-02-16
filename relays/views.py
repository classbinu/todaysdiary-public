from django.shortcuts import render
from django.views.generic.list import ListView
from relays.models import Relay
from posts.models import Post
from comments.models import Comment



class RelayListView(ListView):

    model = Relay
    template_name = "relays/relay_list.html"
    paginate_by = 12
    context_object_name = "relay_list"
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 테스트 서버를 위한 예외처리
        try:
            event_relay = Post.objects.get(id=997)
        except:
            event_relay = Post.objects.get(id=23)

        context["event_relay"] = event_relay
        # user_id = self.request.user.id
        # author = get_object_or_404(User, id=user_id)
        # context["author"] = author
        return context