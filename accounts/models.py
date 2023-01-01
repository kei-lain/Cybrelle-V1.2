from django.db import models
from django.conf import settings

class Industry(models.Model):
    category_name = models.CharField(max_length=240)
    def __str__(self):
        return self.category_name

class Organization(models.Model):
    organization_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    organization_name  = models.CharField(max_length=250, blank=False, null= False)
    industry           = models.ForeignKey(Industry, on_delete=models.CASCADE)
    def __str__(self):
        return self.organization_name
