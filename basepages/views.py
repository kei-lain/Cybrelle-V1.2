from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from django.views.generic import TemplateView, ListView


class homepage(TemplateView):
    template_name = 'home.html'

class aboutpage(TemplateView):
    template_name = 'about.html'

class products_test(ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = 'products'

class articles_test(TemplateView):
    template_name = 'articles.html'


class pricingView(TemplateView):
    template_name = 'pricing.html'
