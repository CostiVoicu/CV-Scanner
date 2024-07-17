from django import forms
from .models import Profile, KeyWord
from django.forms import inlineformset_factory


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name']

class KeyWordForm(forms.ModelForm):
    class Meta:
        model = KeyWord
        fields = ['name', 'value']

KeyWordFormSet = inlineformset_factory(Profile, KeyWord, form=KeyWordForm, extra=1, can_delete=False)