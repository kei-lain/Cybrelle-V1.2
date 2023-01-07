from django.shortcuts import render
import json
import requests
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .models import Host, CVE, Instructions
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
import zipp
from django.urls import  reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Organization
from django.shortcuts import get_object_or_404




# Create your views here.
pk = '' 


class HostsPage(LoginRequiredMixin,CreateView):
    template_name = 'hosts.html'
    model = Host
    success_url = reverse_lazy('dashboard')

class CybrelleDashboard(LoginRequiredMixin,ListView):
    model = Host
    context_object_name = "Hosts"
    template_name = 'dash.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["Hosts"] = Host.objects.all()
        
    #     context["CVES"]  = CVE.objects.all()
    #     context["Instructions"] =  Instructions.objects.all()
        

    #     return context
    

    def get_CVES(self):
        
        for host in Host.objects.count():
            response = requests.get(f"http://127.0.0.1:8000/api/cves/{host}")
            print(response)
            CVEList = []
            CVEList.append(CVE.objects.all(host=host))
            print(CVEList)
        return CVEList
    
    def get_Solution(self, cve_id):
        response = request.get(f'http://127.0.0.1:8000/api/instructions/{cve_id}')
        Instructions = response
        return(Instructions)


        
        

        

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

    


