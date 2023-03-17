from django.shortcuts import render 
from django.urls import  reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegistrationForm

class customRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    # fields =  '__all__'
    redirected_authenticated_user = True
    reverse_lazy =("/login")
    success_url = ("/login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate your Cybrelle.io account'
        message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Set this to a specific email address if desired
            recipient_list=[user.email],
            fail_silently=False,
        )
        return response

    def get_object(self):
        return self.request.user


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')