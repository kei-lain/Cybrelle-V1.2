from django.db import models
from django.conf import settings
# from accounts.models import Organization
from datetime import datetime  
# Create your models here.

class Host(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    host_username = models.CharField(max_length=60)
    host_password = models.CharField(max_length=60)

    linux = 1

    windows = 2

    OSChoices = (linux, "Linux"),(windows,"Windows")

    host_OS = models.PositiveSmallIntegerField(choices=OSChoices, blank=False, null=False)

   
    def __str__(self):
        return self.hostname
    
    

class CVE(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    cves = models.TextField( blank=False, default='CVE-00000-00000')
    info = models.TextField(blank=False, default='To fix you have to ____')
    def __str__(self):
        return self.cves

class Report(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    report = models.TextField(blank=False, default='Enter report here')
    def __str__(self):
        return (f"Report for {self.host}")
    
    
    


    
    
    
    

    
    
