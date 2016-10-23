# from addline.models import *
# from django import forms
# from django.forms import Textarea
#
#
# class DepELAForm(forms.ModelForm):
#
#     class Meta:
#         dependency = forms.ModelMultipleChoiceField(queryset=ExpLineActivity.objects.all())
#         model = ExpLineActDependency
#         fields = ('eLActivity', 'dependentELActivity', 'variant', 'optional')
#         widgets = {
#         }
#         # fields = ()
#         # widgets = {
#         # }
#     # def __init__(self, *args, **kwargs):
#     #     explineid = kwargs.pop('explineid', None)
#     #     super(DepELAForm, self).__init__(*args, **kwargs)
#     #
#     #     if explineid:
#     #         self.fields['dependentELActivity'].choices = ExpLineActivity.objects.filter(expLine__id=explineid)
#
#
#     def save(self, commit=True):
#         activity = super(DepELAForm, self).save(commit=False)
#         for dep in self.dependency:
#             activity.
#         if commit:
#             activity.save()
#         return activity