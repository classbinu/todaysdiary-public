from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportFormView.as_view(), name='report'),
]
