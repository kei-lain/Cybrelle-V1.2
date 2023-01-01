from django.contrib import admin
from django.urls import path, include
from .views import homepage, aboutpage, products_test, articles_test

urlpatterns = [
    path('', homepage.as_view(), name = 'home'),
    path('about/', aboutpage.as_view(), name = 'about'),
    path('products/', products_test.as_view(), name = 'products'),
    path('articles/', articles_test.as_view(), name = 'articles'),

#     path('products/', products.as_view(), name = 'products')
# ]
]