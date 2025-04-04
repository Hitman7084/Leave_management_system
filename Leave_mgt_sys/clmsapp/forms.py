from django import forms
from .models import LeaveApplication, User

class LeaveApprovalForm(forms.ModelForm):
    LEAVE_CHOICES = [
        ("casual", "Casual Leave"),
        ("duty", "Duty Leave"),
        ("medical", "Medical Leave"),
        ("emergency", "Emergency Leave"),
    ]

    leave_type = forms.ChoiceField(
        choices=LEAVE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "std-input"})
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "std-input"}),
        required=True
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "std-input"}),
        required=True
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "std-textarea", "placeholder": "Write your leave request here..."}),
        required=True
    )

    attachment = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={"class": "std-input"}))

    incharge = forms.ModelChoiceField(
        queryset=User.objects.filter(role="Incharge"),
        empty_label="Select Incharge",
        required=True,
        widget=forms.Select(attrs={"class": "std-input"})
    )

    class Meta:
        model = LeaveApplication
        fields = ['incharge', 'leave_type', 'start_date', 'end_date', 'message', 'attachment']


