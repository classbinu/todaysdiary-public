from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='topic'),
]
