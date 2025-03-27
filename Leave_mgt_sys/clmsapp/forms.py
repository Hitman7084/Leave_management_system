from django import forms
from .models import LeaveApplication, User

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['message', 'attachment']  # Exclude student field (auto-assigned)

    incharge = forms.ModelChoiceField(
        queryset=User.objects.filter(role="Incharge"),  # Only fetch users with role "Incharge"
        empty_label="Select Incharge",
        required=True
    )
