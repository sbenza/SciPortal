from addline.models import AbstractWorkflow
from django import forms
from django.forms import Textarea


class AbstractWorkflowForm(forms.ModelForm):
    class Meta:
        model = AbstractWorkflow
        fields = ('name', 'description')
        widgets = {
            'name': Textarea(attrs={'rows': 1,'id': 'wkf-Name', 'required': True, 'placeholder': 'Workflow Name'},),
            'description': Textarea(attrs={'cols': 40, 'rows': 5,'id': 'wkf-Description', 'required': False, 'placeholder': 'Say something about the Workflow...'},),
        }

    def save(self, commit=True):
        workflow = super(AbstractWorkflowForm, self).save(commit=False)
        if commit:
            workflow.save()
        return workflow