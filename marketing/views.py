from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        messages.success(request, "Email received. thank You! ") # message
    return render(request, 'home.html' )