from django.contrib import admin
from django.urls import path, include
from .views import articles_list, article_details
from rest_framework import routers



urlpatterns = [
    path('articles/', articles_list.as_view(), name='blog'),
    path('articles/<int:pk>', article_details.as_view(), name='blog')
    # path('', blog_list.as_view(), name='articles'),
    # path('article/<int:id>', blog_post_view.as_view(), name='article')
    
]
