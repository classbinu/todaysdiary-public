from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mydiary/', views.MydiaryListView.as_view(), name='mydiary'),
    path('diary/<str:username>/', views.DiaryListView.as_view(), name='diary'),
    path('mycomment/', views.MycommentListView.as_view(), name='mycomment'),
    path('comment/<str:username>/', views.CommentListView.as_view(), name='comment'),
    path('mypost_comment/', views.MypostCommentListView.as_view(), name='mypost_comment'),
    path('everydiary/', views.EverydiaryListView.as_view(), name='everydiary'),
    path('intro/', views.IntroTemplateView.as_view(), name='intro'),
    path('notice/', views.NoticeTemplateView.as_view(), name='notice'),
    path('qna/', views.QnaTemplateView.as_view(), name='qna'),
    path('contact/', views.ContactTemplateView.as_view(), name='contact'),
]