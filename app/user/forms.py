from django import forms
from core.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['name', 'password', 'email']
        widgets = {'password': forms.PasswordInput}



class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Feil brukernavn eller passord."),
        'inactive': _("Denne kontoen er inaktiv.")
    }


