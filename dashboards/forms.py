from django import forms
from .models import Host

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = 'hostname','ip_address','host_username', 'host_password', 'host_OS'
