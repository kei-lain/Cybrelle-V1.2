from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

class articles_list(ListView):
    model = Post
    context_object_name = 'articles'
    template_name = 'blog.html'
    reverse_lazy =("/articles")
    success_url = ("/articles")
    

class article_details(DetailView):
    model = Post
    context_object_name = 'article'
    template_name = 'blog-post.html'
    reverse_lazy =("/articles")
    success_url = ("/articles")