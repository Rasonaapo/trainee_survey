from .models import SurveyResponse
from django import forms

class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        exclude = ['ip_address', 'submitted_at', 'survey']
        widgets = {
            'index_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Index Number'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'ghana_card': forms.TextInput(attrs={'class': 'form-control','pattern': '^GHA-\\d{9}-\\d$',
        'title': 'Format: GHA-123456789-1'}),
            'ssnit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'year_admitted': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control',}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', }),
        }

