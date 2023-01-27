from django.urls import path
from .views import Pricing, create_sub, complete, Checkout, cancel

urlpatterns = [
    # path('cancel/', CancelView.as_view(), name='cancel'),
    # path('success/', SuccessView.as_view(), name='success'),
    # path('pricing',PricingPage.as_view(), name='pricing'),
    # path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
    path('pricing/', Pricing.as_view(), name='pricing' ),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('create-sub/', create_sub, name='create-sub'),
    path('complete/', complete, name='complete'),
    path('cancel/', cancel , name='cancel'),


 


]
  

