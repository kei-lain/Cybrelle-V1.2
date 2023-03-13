from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length = 200, required=True, help_text='Organization Name')
    first_name = forms.CharField(max_length = 200, required=True, help_text='First Name')
    last_name = forms.CharField(max_length = 200, required=True, help_text='Last Name')
    email = forms.EmailField(max_length = 200, required=True, help_text='Work Email Address')
    username = forms.CharField(max_length = 200, required=True, help_text='Username')
    password = forms.CharField(widget=forms.PasswordInput, min_length=14, max_length = 32 )
    birth_date = forms.DateField(required=True)
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('organization_name','first_name', 'last_name', 'email' , 'username', 'password', 'birth_date')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user