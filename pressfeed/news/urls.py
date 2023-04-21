from django.urls import path
from . import views

urlpatterns = [
    # path('test/', views.testfeed, name="testfeed"),
    path('feed/', views.newsfeed, name="newsfeed"),
    path('subscribe/', views.subscribe, name="subscribe"),
    path('article/<int:pk>/', views.article_view, name='article-view'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete-comment'),
    path('edit-comment/<int:pk>/', views.edit_comment, name="edit-comment"),
    path('article/<int:pk>/<view>/like/', views.like_article, name='like-article'),
    path('article/<int:pk>/<view>/dislike/', views.dislike_article, name='dislike-article'),
]
