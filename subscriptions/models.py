from django.db import models
from djstripe.models import Customer, Subscription
from django.contrib.auth.models import AbstractUser
from django.conf import settings





# Create your models here.

class User(AbstractUser):  
	
		customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
		subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)
