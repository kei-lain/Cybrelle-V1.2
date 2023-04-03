from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from dashboards.models import Host
from django.urls import path, include
import concurrent.futures
import itertools
from .views import Hosts, CybrelleDashboard, AccountInfo, getVulnerabilities, CVEView, ReportView,  EditHost
from .cybrelle import Scanner
from django.urls import  reverse_lazy
from .api import api
from Cybrelle.custom_decorators import staff_required

# from .api import api



urlpatterns = [
    path('api/', (api.urls)),
    # path('api/getCVE', getCVES),
    # path('api/addCVE/<int:pk>/', addCVES),
    path('dashboard/', CybrelleDashboard.as_view(), name= 'dashboard'),
    path('hosts/', Hosts.as_view(), name='hosts'),
    path('hosts/<int:pk>/', EditHost.as_view(), name= 'edit-host'),
    # path('organization-admin', OrganizationAdmin.as_view(), name='organization-admin'),
    path('accounts-page/<int:pk>', AccountInfo.as_view(), name='accounts-page'),
    path('dashboard/<int:host_id>/', getVulnerabilities, name = 'dashboard'),
    path('cve/<int:pk>/', CVEView.as_view(), name = 'cve-info' ),
    path('report/<int:pk>/', ReportView.as_view(), name='report')
    ]
