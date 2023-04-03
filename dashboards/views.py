from django.shortcuts import render, redirect
from django.db import transaction
from djstripe import webhooks
from .forms import HostForm
import json
import requests
import aiohttp
from aiohttp import web
import asyncio
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
# from rest_framework_api_key.authentication import ApiKeyAuthentication
# from ninja import Router
import os
import aiohttp






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
    reverse_lazy = ("dashboard")
    
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


##correct one works previously

async def getVulnerabilities(request, host_id):
    data = ''
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20000)) as session:
        async with session.post(f"https://cybrelle.io/api/cves/{host_id}") as resp:
            
            if resp.content_type == 'text/plain':
                data = await resp.text()  # retrieve the response as plain text
                # parse the plain text data as needed
            else:
                data = await resp.json()  # assume response content is JSON and parse it accordingly
            while data is not None:
            
                return redirect('dashboard')

# async def getVulnerabilities(request, host_id):
#     data = ''
#     async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20000)) as session:
#         async with session.post(f"http://127.0.0.1:8080/api/cves/{host_id}") as resp:
            
#             if resp.content_type == 'text/plain':
#                 data = await resp.text()  # retrieve the response as plain text
#                 # parse the plain text data as needed
#             else:
#                 data = await resp.json()  # assume response content is JSON and parse it accordingly
#             while data is not None:
            
#                 return redirect('dashboard')

# def getVulnerabilities(request):
#     # host_id = 123 # replace with the actual host ID
#     result = get_Vulnerabilities.delay()
#     return redirect('dashboard')



class ReportView(LoginRequiredMixin,DetailView):
    model = Report
    context_object_name = 'Report'
    template_name = 'repor-page.html'




class AccountInfo(DetailView):
    model = User
    template_name = 'accounts-page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.get_or_create(subscriber=self.request.user)
        user_subscription = Subscription.objects.filter(customer=customer, status="active")
        context["user_subscription"] = user_subscription

        return context


  

    


