from django.shortcuts import render, redirect
from djstripe.models  import Customer

class SubscriptionRequiredMixin():

    """A mixin that checks to see if a user has an active subscription"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.subscription:
                return redirect('/checkout')
            return super().dispatch(request, *args,**kwargs)
        else:
            redirect("/")