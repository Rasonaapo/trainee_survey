from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('', SurveyResponseCreateView.as_view(), name='survey_form'),
    path('success/', TemplateView.as_view(template_name='formsapp/survey_success.html'), name='survey_success'),
    path('closed/', TemplateView.as_view(template_name='formsapp/survey_closed.html'), name='survey_closed'),

]
