from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from dashboards.models import Host
from django.urls import path, include
import concurrent.futures
import itertools
from .views import HostsPage, CybrelleDashboard, OrganizationAdmin, AccountInfo
from .cybrelle import Scanner
from django.urls import  reverse_lazy
from .api import api

# from .api import api



urlpatterns = [
    path('api/', api.urls),
    # path('api/getCVE', getCVES),
    # path('api/addCVE/<int:pk>/', addCVES),
    path('dashboard', CybrelleDashboard.as_view(), name= 'dashboard'),
    path('hosts-page', HostsPage.as_view(), name='hosts-page'),
    path('organization-admin', OrganizationAdmin.as_view(), name='organization-admin'),
    path('accounts-page', AccountInfo.as_view(), name='accounts-page'),
    
]
