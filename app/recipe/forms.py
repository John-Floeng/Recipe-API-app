from django import forms
from django.utils.translation import gettext_lazy as _
from core.models import Recipe


class RecipeForm(forms.ModelForm):
    description = forms.CharField(
        label=_("Beskrivelse"),
        widget=forms.Textarea(attrs={"style": "resize:none;"})
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        help_texts = {
            "tags": "Hold Ctrl nede for å velge flere kategorier",
        }

