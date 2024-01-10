from django import forms
from core.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _






class UserCreationForm(forms.ModelForm):
    
    error_messages = {
        'password_mismatch': _("Passordet matchet ikke, gitt. Prøv igjen."),
    }
    password1 = forms.CharField(label=_("Passord"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Bekreft passord"),
        widget=forms.PasswordInput,
        help_text=_("Fyll inn samme passord igjen for å verifisere."))

    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {'password': forms.PasswordInput}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Feil brukernavn eller passord."),
        'inactive': _("Denne kontoen er inaktiv.")
    }


