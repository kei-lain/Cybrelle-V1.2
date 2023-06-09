"""Cybrelle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from .custom_decorators import staff_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

def staff_check(user):
    return user.is_staff

urlpatterns = [
    path('admin/', (admin.site.urls)),
    path('accounts/', include('accounts.urls')),
    path('', include('blog.urls')),
    path('', include('basepages.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('dashboards.urls')),
    # path('subscription/', include('marketing.urls'),)
    path('',include('subscriptions.urls')),
    path("stripe/", include("djstripe.urls"), name="djstripe"),

    
 
]
