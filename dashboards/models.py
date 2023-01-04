from django.db import models
from django.conf import settings
from accounts.models import Organization
# Create your models here.

class Host(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    host_username = models.CharField(max_length=60)
    host_password = models.CharField(max_length=60)
    def __str__(self):
        return self.hostname
    

class CVE(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    cves = models.TextField( blank=False, default='CVE-00000-00000')
    def __str__(self):
        return self.cves
    
    
    
    

    
    
