from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
import csv
from django.http import HttpResponse

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'contact', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
         ),
    )
admin.site.register(CustomUser, CustomUserAdmin)  # Register the custom user model

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'active', 'created_at']
    list_filter = ['active']
    search_fields = ['bank_name']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['description', 'created_at', 'is_active']
    search_fields = ['description']

@admin.action(description='Export selected survey responses to CSV (uppercase)')
def export_to_csv_uppercase(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_responses_upper.csv"'

    writer = csv.writer(response)
    # Write header
    writer.writerow([
        'Index Number', 'Title', 'First Name', 'Middle Name',
        'Surname', 'Gender', 'Date of Birth', 'Ghana Card Number',
        'SSNIT Number', 'Nationality', 'Program', 'Level',
        'Year Admitted', 'Student Status', 'Email',
        'Bank Name', 'Bank Branch', 'Account Type', 'Account Number',  'Submitted At'
    ])

    for obj in queryset:
        writer.writerow([
            str(obj.index_number).upper(),
            str(obj.title).upper(),
            str(obj.first_name).upper(),
            str(obj.middle_name or '').upper(),
            str(obj.surname).upper(),
            str(obj.gender).upper(),
            obj.date_of_birth.strftime('%Y-%m-%d'),
            str(obj.ghana_card).upper(),
            str(obj.ssnit_number or '').upper(),
            str(obj.nationality).upper(),
            str(obj.program.name).upper(),
            str(obj.level),
            str(obj.year_admitted).upper(),
            str(obj.status).upper(),
            str(obj.email).upper(),
            str(obj.bank.bank_name).upper(),
            str(obj.bank_branch).upper(),
            str(obj.account_type).upper(),
            str(obj.account_number).upper(),
            obj.submitted_at.strftime('%Y-%m-%d %I:%M:%S %p') if obj.submitted_at else ''
        ])

    return response

# Register your models here.
@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    # Show all fields except 'ip_address'
    list_display = (
        'index_number', 'title', 'first_name', 'middle_name', 'surname', 'gender',
        'date_of_birth', 'ghana_card', 'ssnit_number', 'nationality', 'program',
        'level', 'year_admitted', 'status', 'email', 'bank', 'bank_branch',
        'account_type', 'account_number', 'submitted_at'
    )
    search_fields = (
        'index_number', 'first_name', 'surname', 'ghana_card',
        'email', 'account_number'
    )
    list_filter = (
        'program', 'level', 'status', 'gender', 'account_type', 'survey'
    )
    readonly_fields = ('submitted_at', 'ip_address')
    
    actions = [export_to_csv_uppercase]
