from addline.models import ExpLine
from django import forms
from django.forms import Textarea


class ExpLineForm(forms.ModelForm):
    class Meta:
        model = ExpLine
        fields = ('name', 'description')
        widgets = {
            'name': Textarea(attrs={'rows': 1,'id': 'exp-Name', 'required': True, 'placeholder': 'Experiment Name'},),
            'description': Textarea(attrs={'cols': 40, 'rows': 5,'id': 'exp-Description', 'required': False, 'placeholder': 'Say something about the Experiment...'},),
        }

    def save(self, commit=True):
        experiment = super(ExpLineForm, self).save(commit=False)
        if commit:
            experiment.save()
        return experiment