# Generated by Django 5.2.3 on 2025-06-15 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formsapp', '0006_regex_added_to_ghana_card'),
    ]

    def load_survey_initial_record(apps, schema_editor):
        Survey = apps.get_model('formsapp', 'Survey')
        Survey.objects.create(description='Data Colection for Trainee Allowance for 2025 Academic Year')
    
    operations = [
        migrations.RunPython(load_survey_initial_record)
    ]
