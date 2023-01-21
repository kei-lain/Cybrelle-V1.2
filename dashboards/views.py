from django.shortcuts import render, redirect
from .forms import HostForm
import json
import requests
import aiohttp
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse ,HttpResponseForbidden ,HttpRequest
from .models import Host, CVE, Report
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
import zipp
from django.urls import  reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Organization
from django.shortcuts import get_object_or_404
from django.contrib import messages



# Create your views here.
pk = '' 


class Hosts(LoginRequiredMixin,CreateView):
    model = Host
    form = HostForm
    fields = '__all__'
    success_url = reverse_lazy('hosts')
    template_name = 'hosts.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hosts_list"] = Host.objects.filter(user=self.request.user) 
        return context
    

class CybrelleDashboard(LoginRequiredMixin,ListView):
    model = Host
    context_object_name = "Hosts"
    template_name = 'dashboard-main.html'
    # User =get_user_model()
    # user = User.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Hosts"] = Host.objects.filter(user=self.request.user)
        context["CVES"]  = CVE.objects.filter(host__user=self.request.user)
        context["Report"] = Report.objects.filter(host__user=self.request.user)
    #     context["Instructions"] =  Instructions.objects.all()
        return context
    
class CVEView(LoginRequiredMixin, DetailView):
    model = CVE
    context_object_name = 'cve'
    template_name = 'cve-info.html'

def getVulnerabilities(request, host_id):
   
        response =  requests.post(f"http://127.0.0.1:8000/api/cves/{host_id}")
        data = response
        while data is not None:
            return redirect('dashboard')

        # try:
        #     messages.success(response, 'Cybrelle has finished running. The page will now reload to show your vulnerabilities')
        #     return(render(response, 'dashboard-main.html'))
        # except:
        #     messages.success(request, "Something went wrong")
        

# def get_CVES(self) :
    
#     for host in Host.objects.count():
#         response = requests.post(url)(f"http://127.0.0.1:8000/api/cves/{host}")
#         if response.is_val
#         print(CVEList)
#     return CVEList
    
    # def get_Solution(self, cve_id):
    #     response = request.get(f'http://127.0.0.1:8000/api/instructions/{cve_id}')
    #     Instructions = response
    #     return(Instructions)


        
        

        

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

    


