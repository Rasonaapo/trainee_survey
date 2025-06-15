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
    list_display = ['description', 'created_at']
    search_fields = ['description']

# Register your models here.
@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    # Show all fields except 'ip_address'
    list_display = (
        'index_number', 'title', 'first_name', 'middle_name', 'surname', 'gender',
        'date_of_birth', 'ghana_card', 'ssnit_number', 'nationality', 'program',
        'level', 'year_admitted', 'status', 'email', 'bank', 'bank_branch',
        'account_type', 'account_number', 'full_name', 'submitted_at'
    )
    search_fields = (
        'index_number', 'first_name', 'surname', 'ghana_card',
        'email', 'account_number'
    )
    list_filter = (
        'program', 'level', 'status', 'gender', 'account_type', 'survey'
    )
    readonly_fields = ('submitted_at', 'ip_address')
    
    actions = ['export_selected_to_csv']

    def export_selected_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="survey_responses.csv"'

        writer = csv.writer(response)

        # Define fields to export
        fields = [f.name for f in SurveyResponse._meta.fields if f.name not in ['survey', 'submitted_at', 'ip_address']]
        
        # Write headers
        writer.writerow(fields)

        # Write data rows
        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)

        return response

    export_selected_to_csv.short_description = "Export selected responses to CSV"

