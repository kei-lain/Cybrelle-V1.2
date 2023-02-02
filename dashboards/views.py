from django.shortcuts import render, redirect
from django.db import transaction
from djstripe import webhooks
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
from djstripe.models import Subscription, Customer
from django.urls import  reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
# from accounts.models import Organization
from django.shortcuts import get_object_or_404
from django.contrib import messages
from subscriptions.mixins import SubscriptionRequiredMixin




# Create your views here.
pk = '' 


class Hosts(LoginRequiredMixin,CreateView):
  
    model = Host
    fields = 'hostname','ip_address','host_username', 'host_password', 'host_OS'
  
    reverse_lazy =("/hosts")
    success_url = ("/hosts")
    template_name = 'hosts.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.get_or_create(subscriber=self.request.user)
        user_subscription = Subscription.objects.filter(customer=customer, status="active")
        # context["user_subscription"] = Subscription.objects.filter(customer__user=self.request.user, status='active')
        context["user_subscription"] = user_subscription
        context["hosts_list"] = Host.objects.filter(user=self.request.user) 
        return context
    
    @transaction.atomic
    def form_valid(self, form, defaults=None,*args, **kwargs):

        max_host = 0

        form.instance.user = self.request.user
       
     

        customer = Customer.get_or_create(subscriber=self.request.user)
        user_subscription = Subscription.objects.filter(customer=customer, status="active")
        # Get the user's subscription plan
        subscription_plan = Subscription.objects.filter(customer=customer)
        # Check the user's plan
        if subscription_plan.filter(id="price_1MTSIRF8tUfTasHO9EmHLIT3") or subscription_plan.filter(id="price_1MUJ3NF8tUfTasHO0Hza5obs"):
            max_host = 5
        elif subscription_plan.filter(id="price_1MTSJ6F8tUfTasHOmIrwEcEr") or subscription_plan.filter(id="price_1MUJ4BF8tUfTasHOO5nBD7TT"):
            max_host = 10
        elif subscription_plan.filter(id="price_1MUJ4uF8tUfTasHO7olyH7GV") or subscription_plan.filter(id="price_1MTSMxF8tUfTasHOSg8bDYWy"):
            max_host = 20
        else:
            max_host = 5
        # Get the number of host objects the user has already created
        if Host.objects.filter(user=self.request.user).count() >= max_host:
        # if user_host_count + 1 > max_host:
            return redirect('/hosts')
        else:
    
            # while Host.objects.filter(user=self.request.user, hostname=Host.hostname).exists():
            #     pass
            return super().form_valid(form)
    
class EditHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = 'hostname','ip_address','host_username', 'host_password', 'host_OS'
    reverse_lazy =("/hosts")
    success_url = ("/hosts")
    template_name = 'edit_host.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.get_or_create(subscriber=self.request.user)
        user_subscription = Subscription.objects.filter(customer=customer, status="active")
        # context["user_subscription"] = Subscription.objects.filter(customer__user=self.request.user, status='active')
        context["user_subscription"] = user_subscription
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
        customer = Customer.get_or_create(subscriber=self.request.user)
        user_subscription = Subscription.objects.filter(customer=customer, status="active")
        context["user_subscription"] = user_subscription
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
   
        response =  requests.post(f"https://0.0.0.0:8080/api/cves/{host_id}")
        data = response
        while data is not None:
            return redirect('dashboard')


class ReportView(LoginRequiredMixin,DetailView):
    model = Report
    context_object_name = 'Report'
    template_name = 'repor-page.html'




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

# class OrganizationAdmin(LoginRequiredMixin, ListView):
#     model = Organization
#     template_name = 'organization-admin.html'


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

    


