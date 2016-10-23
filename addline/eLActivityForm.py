from addline.models import *
from django import forms
from django.forms import Textarea


class ELActivityForm(forms.ModelForm):
    class Meta:
        model = ExpLineActivity
        fields = ('name', 'operation', 'variant', 'optional', 'expLine')
        widgets = {
            'operation': forms.Select(choices=OPERATION_CHOICES),
            'expLine': forms.HiddenInput(),
            'variant': forms.CheckboxInput(),
            'optional': forms.CheckboxInput()
        }


    def save(self, commit=True):
        activity = super(ELActivityForm, self).save(commit=False)
        if commit:
            activity.save()
        return activity

