from django import forms
from .models import Profile, KeyWord
from django.forms import inlineformset_factory


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name']
        widgets  = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-width'})
        }

class KeyWordForm(forms.ModelForm):
    class Meta:
        model = KeyWord
        fields = ['name', 'value']
        widgets  = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-width'}),
            'value': forms.NumberInput(attrs={'class': 'form-control custom-width'})
        }

KeyWordFormSet = inlineformset_factory(Profile, KeyWord, form=KeyWordForm, extra=1, can_delete=False)