from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mypage/', views.MypageUpdateView.as_view(), name='mypage'),
    path('blacklist/', views.BlacklistTemplateView.as_view(), name='blacklist'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('find_id/', views.FindIdView.as_view(), name='find_id'),
    path('blocked/', views.BlockedUser.as_view(), name='blocked'),
    path('unblocked/', views.UnblockedUser.as_view(), name='unblocked'),
    path('dropout/', views.DropoutView.as_view(), name='dropout'),
]
