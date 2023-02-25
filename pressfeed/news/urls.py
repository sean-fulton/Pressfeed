from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.testfeed, name="testfeed"),
    path('feed/', views.newsfeed, name="newsfeed"),
    path('subscribe/', views.subscribe, name="subscribe")
]
