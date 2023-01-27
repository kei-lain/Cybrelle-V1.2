
from django.views import View
from django.conf import settings
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
import stripe
import djstripe
from django.contrib.auth.decorators import login_required
from djstripe.models import Product, Price, PaymentIntent, Subscription
import json

from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt 

stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

YOUR_DOMAIN = '127.0.0.1:8000'


class Pricing(ListView):
    model = Subscription
    context_object_name = 'subscriptions'

@login_required
def create_sub(request):
  if request.method == 'POST':
      # Reads application/json and returns a response
      data = json.loads(request.body)
      payment_method = data['payment_method']
      stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

      payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
      djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


      try:
          # This creates a new Customer and attaches the PaymentMethod in one API call.
          customer = stripe.Customer.create(
              payment_method=payment_method,
              email=request.user.email,
              invoice_settings={
                  'default_payment_method': payment_method
              }
          )

          djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
          request.user.customer = djstripe_customer
         

          # At this point, associate the ID of the Customer object with your
          # own internal representation of a customer, if you have one.
          # print(customer)

          # Subscribe the user to the subscription created
          subscription = stripe.Subscription.create(
              customer=customer.id,
              items=[
                  {
                      "price": data["price_id"],
                  },
              ],
              expand=["latest_invoice.payment_intent"]
          )

          djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

          request.user.subscription = djstripe_subscription
          request.user.save()

          return JsonResponse(subscription)
      except Exception as e:
          return JsonResponse({'error': (e.args[0])}, status =403)
  else:
    return HTTPresponse('requet method not allowed')

def complete(request):
  return render(request, "subscription/complete.html")

def cancel(request):
  if request.user.is_authenticated:
    sub_id = request.user.subscription.id

    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

    try:
      stripe.Subscription.delete(sub_id)
    except Exception as e:
      return JsonResponse({'error': (e.args[0])}, status =403)
  return redirect("/")

class Checkout(ListView):
	model = Product
	context_object_name = 'products'

	template_name = 'subscription/checkout.html'


