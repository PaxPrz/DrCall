from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.forms.models import model_to_dict
from main.models import User, Notification
from .models import Doctor
from . import forms
from patient.models import Patient, Appointment, Report, Medicine, Prescription
from django.conf import settings
import json, os
from django.contrib import messages
from zoomus import ZoomClient

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
        
class PatientDetailView(DetailView):
    model = Patient
    template_name = 'doctor/patient_detail.html'
    context_object_name = 'patient'
    slug_field = 'user__slug'

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'doctor/list_appointments.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        return self.request.user.doctor.appointment_set.all()

    def post(self, *args, **kwargs):
        action = self.request.POST.get('action')
        act, key = action.split('-')
        a = get_object_or_404(Appointment, pk=int(key))
        if a.doctor == self.request.user.doctor:
            print("ACT:",act)
            if act == "ACCEPT":
                a.accepted = True
            elif act == "CANCEL":
                a.accepted = False
            a.save()
            if settings.NOTIFY:
                Notification.objects.create(
                    notification = "Dr. " + self.request.user.name + " has " + act + "ED your appointment.",
                    user = a.patient.user
                )
        return redirect('doctor:appointments')

class CreateReportView(CreateView):
    model = Report
    template_name = 'doctor/create_report.html'
    form_class = forms.CreateReportForm

    def form_valid(self, form):
        form.save(pt=get_object_or_404(Patient, user__slug=self.kwargs.get('slug')), dt=self.request.user.doctor)
        if settings.NOTIFY:
            Notification.objects.create(
                notification = "Dr. " + self.request.user.name + " has ADDED a report of yours.",
                user = get_object_or_404(User, slug=self.kwargs.get('slug'))
            )
        return redirect('doctor:patientdetail', slug=self.kwargs.get('slug'))

class ReportView(DetailView):
    model = Report
    template_name = 'doctor/report_detail.html'
    context_object_name = 'report'

class CreatePrescriptionView(View):
    model = Prescription
    template_name = 'doctor/create_prescription.html'

    def get(self, *args, **kwargs):
        prescriptionForm = forms.PrescriptionForm()
        medicineFormset = forms.MedicineFormset(queryset=Medicine.objects.none())
        return render(self.request, self.template_name, {'prescriptionForm':prescriptionForm, 'medicineFormset':medicineFormset})

    def post(self, *args, **kwargs):
        prescriptionForm = forms.PrescriptionForm(self.request.POST)
        medicineFormset = forms.MedicineFormset(self.request.POST, self.request.FILES, queryset=Medicine.objects.none())
        if prescriptionForm.is_valid() and medicineFormset.is_valid():
            print("PRES FORM VALID")
            pres = prescriptionForm.save(commit=False)
            pres.doctor = self.request.user.doctor
            pres.patient = get_object_or_404(Patient, user__slug=self.kwargs.get('slug'))
            pres.save()
            if settings.NOTIFY:
                Notification.objects.create(
                    notification = "Dr. " + self.request.user.name + " has DIAGNOSED your condition.",
                    user = get_object_or_404(User, slug=self.kwargs.get('slug'))
                )

            for medForm in medicineFormset.cleaned_data:
                print("ADDING MEDS")
                name = medForm.get('name')
                dose = medForm.get('dose', 'unknown')
                days = medForm.get('days', 0)
                if name!=None:
                    Medicine.objects.create(name=name, dose=dose, days=days, prescription=pres)
        else:
            print("PrescriptionErrors: ", prescriptionForm.errors)
            print("MedicineformsetErrors: ", medicineFormset.errors)
            return render(self.request, self.template_name, {'prescriptionForm':prescriptionForm, 'medicineFormset':medicineFormset})
        return redirect('doctor:patientdetail', slug=self.kwargs.get('slug'))
                
class NotificationListView(ListView):
    model = Notification
    template_name = 'doctor/list_notification.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notification_set.all()

class MakeCall(View):
    def get(self, *args, **kwargs):
        pk = int(self.request.GET.get('appid'))
        a = get_object_or_404(Appointment, id=pk)
        SUCCESS=False
        if a.link == "no":
            client = ZoomClient(os.environ.get('KEY'), os.environ.get('SECRET'))
            x = client.user.list()
            if x.status_code==200:
                c = json.loads(x.content)
                uid = c['users'][0]['id']
                m = client.meeting.create(user_id=uid)
                if m.status_code==201:
                    j = json.loads(m.content)
                    a.link = j['start_url']
                    a.save()
                    SUCCESS=True
                    Notification.objects.create(
                        notification = 'Dr. '+self.request.user.name+' has started the call. Join ASAP!',
                        user = a.patient.user
                    )
                    messages.success(self.request, "Call Created! Join to visit Zoom call!")
        if not SUCCESS:
            messages.error(self.request, "Couldn't start call! Try again later!")
        return redirect('doctor:appointments')
            

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
