from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms.models import model_to_dict
from main.models import User
from .models import Patient
from . import forms
from doctor.models import Doctor

# Create your views here.
class PatientCreationView(CreateView):
    template_name = 'patient/signup.html'
    model = User
    form_class = forms.PatientCreationForm
    success_url = reverse_lazy('main:login')

    def form_valid(self, form):
        print("PATIENT SIGNUP FORM VALID")
        response = super().form_valid(form)
        patient = Patient.objects.create(user=self.object)
        return response

    def form_invalid(self, form):
        print("PATIENT SIGNUP FORM INVALID")
        return super().form_invalid(form)

class DashBoardView(TemplateView):
    template_name = 'patient/dashboard.html'

class PatientProfileUpdate(TemplateView):
    template_name = 'patient/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = self.request.user
        i = model_to_dict(u)
        context["form"] = forms.PatientUpdateForm(initial=i)
        return context
    
    def post(self, *args, **kwargs):
        form = forms.PatientUpdateForm(data=self.request.POST, files=self.request.FILES, instance=self.request.user)
        if form.is_valid():
            print("PATIENT UPDATE FORM VALID")
            form.save(user=self.request.user)
            return redirect('patient:dashboard')
        return render(self.request, self.template_name, {'form':form})

class DoctorListView(ListView):
    model = Doctor
    context_object_name = 'doctors'
    template_name = 'patient/search.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.ProfileSearchForm()
        return context
    
    def get_queryset(self):
        # if self.form.is_valid():
        #     print("DOCTORLIST FORM VALID")
        #     print(self.form.cleaned_data['name'])
        return Doctor.objects.all()
    
class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'patient/doctor_detail.html'
    slug_field = 'user__slug'
    
    # def get_object(self):
    #     return get_object_or_404(Doctor, user__slug=self.kwargs['slug'])

