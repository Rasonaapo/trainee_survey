from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView
from .models import SurveyResponse, Survey
from .forms import SurveyResponseForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
class SurveyResponseCreateView(CreateView):
    model = SurveyResponse
    template_name = 'formsapp/survey_form.html'
    form_class = SurveyResponseForm
    success_url = reverse_lazy('survey_success')  # new line

    def dispatch(self, request, *args, **kwargs):
        # check if there is an active survey
        if not Survey.objects.filter(is_active=True).exists():
            return redirect('survey_closed')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # IP address is captured here
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
        instance = form.save(commit=False)
        instance.ip_address = ip

        # Assign the default survey instance prefilled through migration.. This will change in the future as an Admin will make active a survey and vice versa
        instance.survey = Survey.objects.first()  
        instance.save()

        #return super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('survey_success'))


    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)  # Print form errors to debug
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Data Collection for Trainee Allowance'

        return context

