from django.db import models
from django.conf import settings
from django.contrib.auth.models import User




# class Industry(models.Model):
#     category_name = models.CharField(max_length=240)
#     def __str__(self):
#         return self.category_name

# class Organization(models.Model):
#     users = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     organization_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='users')
#     organization_name  = models.CharField(max_length=250, blank=False, null= False)
#     # industry           = models.ForeignKey(Industry, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.organization_name

