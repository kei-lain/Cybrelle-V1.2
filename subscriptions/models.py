from django.db import models
from djstripe.models import Customer, Subscription
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid





# Create your models here.

class User(AbstractUser):  
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='djstripe_customer',
    )
    subscription = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='djstripe_subscription',
    )
  


   
	
	