from addline.models import *
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


# class ELActivityForm(forms.ModelForm):
#     class Meta:
#         model = ExpLineActivity
#         fields = ('name', 'operation', 'variant', 'optional', )
#         exclude = ('expLine',)
#         widgets = {
#             'name': Textarea(attrs={'rows': 1,'id': 'name', 'required': True, 'placeholder': 'Activity Name'},),
#             'operation': forms.Select(choices=OPERATION_CHOICES, attrs={'id': 'operation'}),
#             # 'expLine': forms.HiddenInput(attrs={'id': 'expLine'}),
#             'variant': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'id': 'variant'}),
#             'optional': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'id': 'optional'})
#             # 'operation':
#         }
#
#
#     def save(self, commit=True):
#         activity = super(ELActivityForm, self).save(commit=False)
#         if commit:
#             activity.save()
#         return activity
#
#
# class AbstractWorkflowForm(forms.ModelForm):
#     class Meta:
#         model = AbstractWorkflow
#         fields = ('name', 'description')
#         widgets = {
#             'name': Textarea(attrs={'rows': 1,'id': 'wkf-Name', 'required': True, 'placeholder': 'Workflow Name'},),
#             'description': Textarea(attrs={'cols': 40, 'rows': 5,'id': 'wkf-Description', 'required': False, 'placeholder': 'Say something about the Workflow...'},),
#         }
#
#     def save(self, commit=True):
#         workflow = super(AbstractWorkflowForm, self).save(commit=False)
#         if commit:
#             workflow.save()
#         return workflow
#
#
#
#
#
# class AbstractActivityForm(forms.ModelForm):
#     class Meta:
#         model = ExpLineActivity
#         fields = ('name', 'operation', 'description', )
#         widgets = {
#             'name': Textarea(attrs={'rows': 1,'id': 'aact-name', 'required': True, 'placeholder': 'Activity Name'},),
#             'description': Textarea(attrs={'rows': 1,'id': 'aact-description', 'required': True, 'placeholder': 'Say something about the activity...'},),
#             'operation': forms.Select(choices=OPERATION_CHOICES, attrs={'id': 'aact-operation'}),
#         }
#
#
#     def save(self, commit=True):
#         activity = super(AbstractActivityForm, self).save(commit=False)
#         if commit:
#             activity.save()
#         return activity
#
