from django import forms
from core.models import User


class UserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['name', 'password', 'email']
        widgets = {'password': forms.PasswordInput}


