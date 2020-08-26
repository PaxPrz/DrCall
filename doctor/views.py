from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.forms.models import model_to_dict
from main.models import User
from .models import Doctor
from . import forms

# Create your views here.
class DoctorCreationView(CreateView):
    template_name = 'doctor/signup.html'
    model = User
    form_class = forms.DoctorCreationForm
    success_url = reverse_lazy('main:login')

    def form_valid(self, form):
        print("FORM VALID")
        response = super().form_valid(form)
        doctor = Doctor.objects.create(user=self.object)
        return response

    def form_invalid(self, form):
        print("FORM INVALID")
        return super().form_invalid(form)

class DashBoardView(TemplateView):
    template_name = 'doctor/dashboard.html'

class DoctorProfileUpdate(TemplateView):
    template_name = 'doctor/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = self.request.user
        i = model_to_dict(u.doctor)
        i.update(model_to_dict(u))
        context["form"] = forms.DoctorUpdateForm(initial=i)
        return context
    
    def post(self, *args, **kwargs):
        form = forms.DoctorUpdateForm(data=self.request.POST, files=self.request.FILES, instance=self.request.user)
        if form.is_valid():
            print("UPDATE FORM VALID")
            form.save(user=self.request.user)
            return redirect('doctor:dashboard')
        return render(self.request, self.template_name, {'form':form})
        
    

# class DoctorProfileUpdate(UpdateView):
#     template_name = 'doctor/profile.html'
#     model = Doctor
#     form_class = forms.DoctorUpdateForm
#     success_url = reverse_lazy('doctor:dashboard')

#     def get_object(self, queryset=None):
#         return self.request.user

#     def form_valid(self, form):
#         print("PROFILE FORM VALID")
#         if self.request.method == "POST":
#             f = forms.DoctorUpdateForm(form, instance=self.request.user)
#             f.save()
#         else:
#             f = form
#         return super().form_valid(f)
