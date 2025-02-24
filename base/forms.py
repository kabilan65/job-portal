from django import forms
from .models import Job_alerts

class JobAlertForm(forms.ModelForm):
    class Meta:
        model = Job_alerts
        fields = ['job_type', 'location', 'keyword']