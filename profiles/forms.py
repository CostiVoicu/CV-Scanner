from django import forms
from .models import Profile, KeyWord
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name']
        widgets  = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-width'})
        }
        labels = {
            "name": "Name:"
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name[0].isdigit():
            raise ValidationError('Name can\'t be a digit.')
        
        return name

class KeyWordForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name[0].isdigit():
            raise ValidationError('Name can\'t be a digit.')
        
        return name
    
    def clean_value(self):
        value = self.cleaned_data['value']
        if value == 0:
            raise ValidationError('Value can\'t be zero.')
        if value < 0:
            raise ValidationError('Value can\'t be negative.')
        
        return value

    class Meta:
        model = KeyWord
        fields = ['name', 'value']
        widgets  = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-width'}),
            'value': forms.NumberInput(attrs={'class': 'form-control custom-width'})
        }
        
        labels = {
            "name": "Name:",
            "value": "Value:",
        }

class RequiredFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        if not any(form.cleaned_data for form in self.forms):
            raise ValidationError('Please add at least one keyword.')
        
        

KeyWordFormSet = inlineformset_factory(Profile, KeyWord, form=KeyWordForm, formset=RequiredFormSet, extra=1, can_delete=False)