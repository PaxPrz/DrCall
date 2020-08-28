from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.forms.models import model_to_dict
from main.models import User, Notification
from .models import Patient, Rating, Appointment, Report, ReportImage, Prescription, Medicine
from . import forms
from doctor.models import Doctor
import datetime
from django.forms import modelform_factory
from django.contrib import messages
from django.conf import settings
from zoomus import ZoomClient
import os,json

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
            form.save()
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
    context_object_name = 'doctor'

    # def get_object(self):
    #     return get_object_or_404(Doctor, user__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            r = self.request.user.patient.rating.get(doctor=get_object_or_404(Doctor, user__slug=self.kwargs['slug']))
            rating = r.rating
        except:
            rating = 0
        context["myRating"] = str(rating)
        return context
    

    def post(self, *args, **kwargs):
        if self.request.POST.get('subscribe') == "Add Doctor":
            self.request.user.patient.allowed_doctor.add(get_object_or_404(Doctor, user__slug=self.kwargs['slug']))
            if settings.NOTIFY:
                Notification.objects.create(
                    notification = "You have got a new Patient: "+self.request.user.name +".",
                    user = get_object_or_404(User, slug=self.kwargs.get('slug'))
                )
        elif self.request.POST.get('subscribe') == "Remove Doctor":
            self.request.user.patient.allowed_doctor.remove(get_object_or_404(Doctor, user__slug=self.kwargs['slug']))
        if self.request.POST.get('rating') != None:
            rating = int(self.request.POST.get('rating'))
            print("RATING: ",rating)
            if rating < 1:
                rating = 1
            if rating > 5:
                rating = 5
            try:
                r = self.request.user.patient.rating.get(doctor=get_object_or_404(Doctor, user__slug=self.kwargs['slug']))
                r.rating = rating
                r.save()
            except:
                r = Rating.objects.create(doctor=get_object_or_404(Doctor, user__slug=self.kwargs['slug']), rating=rating)
                self.request.user.patient.rating.add(r)
        return redirect('patient:doctordetail', slug=self.kwargs['slug'])

class MakeAppointmentView(TemplateView):
    template_name = 'patient/make_appointment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.MakeAppointmentForm()
        return context

    def post(self, *args, **kwargs):
        form = forms.MakeAppointmentForm(self.request.POST)
        if form.is_valid():
            print("FORM VALID")
            form.save(pt=self.request.user.patient, dt=get_object_or_404(Doctor, user__slug=self.kwargs.get('slug')))
            if settings.NOTIFY:
                Notification.objects.create(
                    notification = self.request.user.name + " has SET an appointment with you.",
                    user = get_object_or_404(User, slug=self.kwargs.get('slug'))
                )
            return redirect('patient:appointments')
        print(self.request.POST.get('appointment_time'))
        return render(self.request, self.template_name, {'form':form})

class ListAppointmentView(ListView):
    model = Appointment
    template_name = 'patient/list_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return self.request.user.patient.appointment_set.all()
    
class ListReportView(ListView):
    model = Report
    template_name = 'patient/list_reports.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return self.request.user.patient.report_set.all()


class CreateReportView(CreateView):
    model = Report
    template_name = 'patient/create_report.html'
    success_url = reverse_lazy('patient:reports')
    form_class = forms.CreateReportForm

    def form_valid(self, form):
        form.save(pt=self.request.user.patient)
        return redirect(self.success_url)

class ReportDetailView(DetailView):
    model = Report
    template_name = 'patient/report_detail.html'
    context_object_name = 'report'

class PrescriptionView(ListView):
    model = Prescription
    template_name = 'patient/list_prescription.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        return self.request.user.patient.prescription_set.all()
    
class NotificationListView(ListView):
    model = Notification
    template_name = 'patient/list_notification.html'
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
                        notification = self.request.user.name+' has started the call. Join ASAP!',
                        user = a.doctor.user
                    )
                    messages.success(self.request, "Call Created! Join to visit Zoom call!")
        if not SUCCESS:
            messages.error(self.request, "Couldn't start call! Try again later!")
        return redirect('patient:appointments')

# class CreateReportView(View):
#     model = Report
#     template_name = 'patient/create_report.html'
    
#     def get(self, *args, **kwargs):
#         ReportImageFormset = modelformset_factory(ReportImage, form=forms.CreateReportImageForm)
#         reportForm = forms.CreateReportForm(queryset=ReportImage.objects.none())
#         imageset = ReportImageFormset()
#         return render(self.request, self.template_name, {'reportForm':reportForm, 'formset':imageset})
    
#     def post(self, *args, **kwargs):
#         ReportImageFormset = modelformset_factory(ReportImage, form=forms.CreateReportImageForm)
#         reportForm = forms.CreateReportForm(self.request.POST)
#         imageset = ReportImageFormset(self.request.POST, self.request.FILES)
#         if reportForm.is_valid() and imageset.is_valid():
#             report = reportForm.save(commit=False)
#             report.patient = self.request.user.patient
#             # report.save()

#             print("imgaset:",imageset.cleaned_data)
#             for form in imageset.cleaned_data:
#                 print(type(form))
#                 image = form.get('image')
#                 photo = ReportImage(report=report, image=image)
#                 photo.save()
#             messages.success(self.request, "Report Created!")
#         else:
#             print(reportForm.errors)
#             print(imageset.errors)
#             return render(self.request, self.template_name, {'reportForm':reportForm, 'formset':imageset})
#         return redirect('patient:reports')

    