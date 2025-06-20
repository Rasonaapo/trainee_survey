from .models import SurveyResponse
from django import forms
import re

class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        exclude = ['ip_address', 'submitted_at', 'survey', 'full_name']
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
        }

    # Ministry of Education requires index numbers to follow a specific format
    def clean_index_number(self):
        index_number = self.cleaned_data['index_number']
        pattern = r'^COH(202[0-4])(\d{2}[A-Za-z]?)(\d{3})$'

        if not re.match(pattern, index_number):
            raise forms.ValidationError(
                "Index number must follow this pattern: COH + year (2020-2024) + 2 digits (optionally 1 letter) + 3 digits. Eg. COH202003S002"
            )
        return index_number

    # account number be from 7 (min) to 16 (max) digits
    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']

        if not account_number.isdigit():
            raise forms.ValidationError("Account number must contain only digits.")
        if not (7 <= len(account_number) <= 16):
            raise forms.ValidationError("Account number must be between 7 and 16 digits.")
        
        return account_number