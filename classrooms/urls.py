from django.urls import path
from . import views

app_name = 'classrooms'

urlpatterns = [
    path('', views.ClassroomListView.as_view(), name='classroom_list'),
    path('create/', views.ClassroomCreateView.as_view(), name='classroom_create'),
    path('search/', views.ClassroomSearchView.as_view(), name='classroom_search'),
    path('failed/', views.ClassroomFailedView.as_view(), name='classroom_failed'),
    path('<int:pk>/', views.ClassroomDetailView.as_view(), name='classroom_detail'),
    path('<int:pk>/in/', views.ClassroomInView.as_view(), name='classroom_in'),
    path('<int:pk>/out/', views.ClassroomOutView.as_view(), name='classroom_out'),
    path('<int:pk>/update/', views.ClassroomUpdateView.as_view(), name='classroom_update'),
    path('<int:pk>/member/', views.ClassroomMemberView.as_view(), name='classroom_member'),
    path('<int:pk>/password/', views.ClassroomPasswordView.as_view(), name='classroom_password'),
    path('<int:pk>/ban/', views.ClassroomBanView.as_view(), name='classroom_ban'),
    path('<int:pk>/delete/', views.ClassroomDeleteView.as_view(), name='classroom_delete'),
]
