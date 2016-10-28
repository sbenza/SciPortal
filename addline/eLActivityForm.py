from addline.models import *
from django import forms
from django.forms import Textarea, RadioSelect


class ELActivityForm(forms.ModelForm):
    class Meta:
        model = ExpLineActivity
        fields = ('name', 'operation', 'variant', 'optional', )
        exclude = ('expLine',)
        widgets = {
            'name': Textarea(attrs={'rows': 1,'id': 'name', 'required': True, 'placeholder': 'Activity Name'},),
            'operation': forms.Select(choices=OPERATION_CHOICES, attrs={'id': 'operation'}),
            # 'expLine': forms.HiddenInput(attrs={'id': 'expLine'}),
            'variant': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'id': 'variant'}),
            'optional': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'id': 'optional'})
            # 'operation':
        }


    def save(self, commit=True):
        activity = super(ELActivityForm, self).save(commit=False)
        if commit:
            activity.save()
        return activity

