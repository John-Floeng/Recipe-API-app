from django import forms

from core.models import Recipe


class RecipeForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={"style": "resize:none;"})
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        help_texts = {
            "tags": "Hold Ctrl nede for å velge flere kategorier",
        }

