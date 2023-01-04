from django.shortcuts import render
import json
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .models import Host, CVE
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
import zipp
from django.urls import  reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Organization
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from .serializers import HostSerializer, CVESerializer
from .cybrelle import Scanner, execute



# Create your views here.
pk = '' 


class HostsPage(LoginRequiredMixin,CreateView):
    template_name = 'hostspage.html'
    model = Host
    success_url = reverse_lazy('dashboard')

class CybrelleDashboard(LoginRequiredMixin,ListView):
    model = Host
    template_name = 'cybrelle_dashboard.html'
    # def get_vuls(request):
    #     get_vulns_response = requests.get('127.0.0.1:8001/')
    #     get_vulns_response = json.loads(get_vulns_response)
    #     return(render(request,get_vulns_response))

class OrganizationAdmin(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization-admin.html'


class AccountInfo(DetailView):
    model = User
    template_name = 'accounts-page.html'


@api_view(['GET'])
def gethosts(requests):
    hosts = Host.objects.all()
    serializer = HostSerializer(hosts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getCVES(request):
    cves = CVE.objects.all()
    serializer = CVESerializer(cves, many=True)
    return Response(serializer.data)

@api_view(['GET','POST', 'PUT'])
def addCVES( request, pk ):
    obj = get_object_or_404(Host, pk=pk)
    hosts = Host.objects.filter(pk=pk)
    host_for_cve = obj.hostname
    user = obj.user
    hostname= obj.hostname
    Organization = obj.organization
    host_username = obj.host_username
    host_password = obj.host_password
    ip_address = obj.ip_address
    scan_results = execute(ip_address, host_username, host_password)
    new_CVE = CVE.objects.create(host=obj, user=user, Organization=Organization, cves=scan_results)
    new_CVE.save()
    serializer = CVESerializer(new_CVE)
    return Response(serializer.data)


    # host = Host.objects.get(pk=pk)
    # user = host.user
    # obj = get_object_or_404(Host, pk=pk)
    # organization = obj.organization
    # ip_address = str(obj.ip_address)
    # host_username = obj.host_username
    # host_password = obj.host_password
    # serializer = CVESerializer(data=request.data)
    # if serializer.is_valid():
    #     host = serializer.data.host
    #     organization = serializer.data.Organization
    #     user = serializer.data.user
    #     cves = scan_results
    #     queryset = CVE.objects.filter(host=host)
    #     room = queryset[0]
    #     if queryset.exists():
    #         cves = scan_results
    #         room.save(update_fields['cves'])
    #     else:

    


