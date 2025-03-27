from django import forms
from .models import LeaveApplication

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['message', 'attachment']
