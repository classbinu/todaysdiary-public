from django.urls import path
from . import views

app_name = 'relays'

urlpatterns = [
    path('', views.RelayListView.as_view(), name='relay_list'),
]
