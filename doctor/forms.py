from django import forms
from .models import Doctor
from main.models import User
from django.contrib.auth.forms import UserCreationForm

class DoctorCreationForm(UserCreationForm):
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(str(self.cleaned_data['email'])+' already exists!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['name', 'username', 'contact', 'gender', 'email', 'password1', 'password2']

class DoctorUpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=50, required=False)
    location = forms.CharField(label="Location", max_length=50, required=False)
    dob = forms.DateField(label="Date of Birth", required=False)
    contact = forms.CharField(label="Contact no.", max_length=15, required=False)
    profile_pic = forms.ImageField(label="Profile Picture", required=False)

    def save(self, user, *args, **kwargs):
        user.doctor.description = self.cleaned_data['description']
        user.doctor.speciality.set(self.cleaned_data['speciality'])
        user.doctor.education.set(self.cleaned_data['education'])
        user.doctor.hospital.set(self.cleaned_data['hospital'])
        user.doctor.save()
        super().save(*args, **kwargs)

    class Meta:
        model = Doctor
        fields = ['name','description', 'location', 'dob', 'contact', 'speciality', 'education', 'hospital', 'profile_pic']