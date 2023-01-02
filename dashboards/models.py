from django.db import models
from django.conf import settings
from accounts.models import Organization
# Create your models here.

class Host(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    host_username = models.CharField(max_length=60)
    host_password = models.CharField(max_length=60)
    def __str__(self):
        return self.ip_address

class CVE(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    CVE = models.CharField(max_length=60)
    

    
    
