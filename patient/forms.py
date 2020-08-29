from django import forms
from .models import Patient, Appointment, Report, ReportImage, Prescription, Medicine
from main.models import User
import datetime
from django.contrib.auth.forms import UserCreationForm

class PatientCreationForm(UserCreationForm):
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(str(self.cleaned_data['email'])+' already exists!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['name', 'username', 'contact', 'gender', 'email', 'password1', 'password2']


class PatientUpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=50, required=False)
    location = forms.CharField(label="Location", max_length=50, required=False)
    dob = forms.DateField(label="Date of Birth", required=False)
    contact = forms.CharField(label="Contact no.", max_length=15, required=False)
    profile_pic = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = Patient
        fields = ['name', 'location', 'dob', 'contact', 'profile_pic']

SEARCH_CHOICES = (
    ('1', 'Name'),
    ('2', 'Speciality'),
    ('3', 'Hospital'),
)

class ProfileSearchForm(forms.Form):
    name = forms.CharField(required=False)
    choice = forms.ChoiceField(choices=SEARCH_CHOICES, required=True, initial='1')

class MakeAppointmentForm(forms.ModelForm):
    problem = forms.CharField(widget=forms.Textarea(attrs={
            'width': '50%',
            'height': '30px',
    }))
    appointment_time = forms.DateTimeField(label="Appointment Time", required=True,
        input_formats=["%m/%d/%Y %I:%M %p",
            "%m/%d/%Y %H:%M:%S"],
        widget = forms.DateTimeInput(
            attrs={
                'class':'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
            }
        )
    )

    def clean_time(self):
        time = self.cleaned_data['appointment_time']
        if time <= datetime.datetime.now():
            raise forms.ValidationError("The date cannot be in the past!")
        return time

    def save(self, pt, dt, *args):
        m = super(MakeAppointmentForm, self).save(commit=False)
        m.patient = pt
        m.doctor = dt
        m.save()
        return m

    class Meta:
        model = Appointment
        fields = ['problem', 'appointment_time']

class CreateReportForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control',
        }
    ))

    def save(self, pt):
        r = super(CreateReportForm, self).save(commit=False)
        r.patient = pt
        r.save()
        return r

    class Meta:
        model = Report
        fields = ['title', 'date', 'institute', 'content', 'image']

class CreateReportImageForm(forms.ModelForm):
    
    # def save(self, rep):
    #     i = super(CreateReportImageForm, self).save(commit=False)
    #     i.report = rep
    #     i.save()
    #     return i

    class Meta:
        model = ReportImage
        fields = ['image']
