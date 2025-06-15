from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView
from .models import SurveyResponse, Survey
from .forms import SurveyResponseForm
from django.urls import reverse_lazy

# Create your views here.
class SurveyResponseCreateView(CreateView):
    model = SurveyResponse
    template_name = 'formsapp/survey_form.html'
    form_class = SurveyResponseForm
    success_url = reverse_lazy('survey_success')  # new line

    def form_valid(self, form):
        # Optionally add the IP address capture here
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
        instance = form.save(commit=False)
        instance.ip_address = ip

        # Assign the default survey instance prefilled through migration.. This will change in the future as an Admin will make active a survey
        instance.survey = Survey.objects.first()  # Assuming you have a default survey instance
        instance.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)  # Print form errors to debug
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Data Collection for Trainee Allowance'

        return context

