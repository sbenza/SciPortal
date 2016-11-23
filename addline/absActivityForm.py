from addline.models import *
from django import forms
from django.forms import Textarea, RadioSelect


class AbstractActivityForm(forms.ModelForm):
    class Meta:
        model = AbstractActivity
        fields = ('name', 'description', 'operation')
        widgets = {
            'operation': forms.HiddenInput(),
            'name': Textarea(attrs={'rows': 1,'id': 'aact-name', 'required': True, 'placeholder': 'Activity Name'},),
            'description': Textarea(attrs={'rows': 1,'id': 'aact-description', 'required': True, 'placeholder': 'Say something about the activity...'},),
        }


    def save(self, commit=True):
        activity = super(AbstractActivityForm, self).save(commit=False)
        if commit:
            activity.save()
        return activity

