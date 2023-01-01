from django.contrib import admin
from django.urls import path, include
from .views import articles_list, article_details
from rest_framework import routers



urlpatterns = [
    path('articles/', articles_list.as_view(), name='articles'),
    path('articles/<int:id>', article_details.as_view(), name='articles <id>')
    # path('', blog_list.as_view(), name='articles'),
    # path('article/<int:id>', blog_post_view.as_view(), name='article')
    
]
