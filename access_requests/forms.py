from django import forms
from .models import AccessRequest


class AccessRequestForm(forms.ModelForm):

    class Meta:
        model = AccessRequest

        fields = [
            'reason',
            'duration_days',
        ]

        widgets = {

            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Explain why you need this access...'
                }
            ),

            'duration_days': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'placeholder': 'Example: 30'
                }
            ),
        }

        labels = {
            'reason': 'Reason for Access',
            'duration_days': 'Access Duration (Days)',
        }