from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('search/', views.search, name='search'),
    path('breach/', views.breach, name='breach'),
    path('edit/<int:empID>/', views.edit, name='edit'),
    path('generate/<int:empID>/', views.generate, name='generate'),
]